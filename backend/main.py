from flask import Flask, jsonify, request
from extensions import db
from config import Config
from flask_migrate import Migrate
from models import User, Expense
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import date
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import func
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate = Migrate(app,db)
    jwt = JWTManager(app)
    CORS(app)

    @app.route('/')
    def index(): 
        return jsonify({'message': 'Budgett API running!'}), 200

    @app.route('/api/register', methods=["POST"])
    def register():
        response = request.get_json()
        email = response.get('email', '').strip()
        password = response.get('password', '').strip()

        #check empty submit
        if not email or not password:
            return jsonify({"error": "empty email or password"}), 400

        #validate unique email
        email_exists = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if email_exists:
            return jsonify({'error': 'email already exists'}), 409
        
        # hash password, create new user
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(email=email, password_hash=password_hash.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': 'new user created'}), 201


    @app.route('/api/login', methods=["POST"])
    def login():
        response = request.get_json()
        input_email = response.get('email', '').strip()
        input_password = response.get('password', '').strip()

        user = db.session.execute(db.select(User).where(User.email == input_email)).scalar()

        if user and user.password_hash and bcrypt.checkpw(input_password.encode('utf-8'), user.password_hash.encode('utf-8')):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({'access_token': access_token}), 200
        else: 
            return jsonify({'error': 'unauthorized'}), 401

    GOOGLE_CLIENT_ID = '605039480451-79spfo1apkqvfo2foq6aq6t59002osob.apps.googleusercontent.com'
    @app.route('/api/auth/google', methods=["POST"])
    def google_auth():
        body = request.get_json()
        credential = body.get('credential')

        if not credential:
            return jsonify({'error': 'missing credentials'}), 400
        
        try:
            idinfo = id_token.verify_oauth2_token(credential, google_requests.Request(), GOOGLE_CLIENT_ID)
        except ValueError:
            return jsonify({'error': 'invalid token'}), 401
        
        google_id = idinfo.get('sub')
        email = idinfo.get('email')

        user = db.session.execute(db.select(User).where(User.google_id == google_id)).scalar()
        
        if not user:
            existing = db.session.execute(db.select(User).where(User.email == email)).scalar()

            if existing:    # if user exists and password
                if existing.password_hash:
                    return jsonify({'error': 'email is already registered with password'}), 409 


            # step 6: if email not found in db, make new user
            user = User(email=email, google_id=google_id, password_hash=None)
            db.session.add(user)
            db.session.commit()

        access_token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': access_token}), 200


    # LOGIN REQUIRED ROUTES
        
    # GET EXPENSES
    PER_PAGE = 10
    @app.route('/api/expenses', methods=["GET"])
    @jwt_required()
    def get_expense():
        user_id = int(get_jwt_identity())
        query = db.select(Expense).where(Expense.user_id == user_id)
        
        category = request.args.get('category')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        if category:
            query = query.where(Expense.category == category)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                query = query.where(Expense.expense_date >= start_date)
            except ValueError:
                return jsonify({"error": "invalid format"}), 400


        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                query = query.where(Expense.expense_date <= end_date)
            except ValueError:
                return jsonify({"error": "invalid format"}), 400
            
        # total results from query
        query = query.order_by(Expense.created_at.desc())
        total = db.session.scalar(db.select(func.count()).select_from(query.subquery()))
        try:
            page = int(request.args.get('page', 1))
            if page < 1:
                raise ValueError
        except ValueError:
            return jsonify({"error": "page must be a positive integer"}), 400
        
        query = query.limit(PER_PAGE).offset((page - 1) * PER_PAGE)
        expenses = db.session.execute(query).scalars().all()

        return jsonify({"expenses": [expense.to_dict() for expense in expenses], 
                        "pagination": {
                            "page": page,
                            "per_page": PER_PAGE,
                            "total": total,
                            "total_pages": (total + PER_PAGE - 1) // PER_PAGE
                        }
                        }), 200

    @app.route('/api/expenses/<int:expense_id>', methods=['GET'])
    @jwt_required()
    def get_single_expense(expense_id):
        user_id = int(get_jwt_identity())
        expense = db.get_or_404(Expense, expense_id)

        if expense.user_id != user_id:
            return jsonify({'error': 'Forbidden'}), 403
        
        return jsonify(expense.to_dict()), 200 

    # POST EXPENSE
    @app.route('/api/expenses', methods=["POST"])
    @jwt_required()
    def post_expense():
        user_id = int(get_jwt_identity())

        post_body = request.get_json()
        name = post_body.get('name')
        amount = post_body.get('amount')
        category = post_body.get('category')
        expense_date_str = post_body.get('expense_date')

        if not name or amount is None or not category or not expense_date_str:
            return jsonify({'error': 'missing required fields'}), 400
        
        try:
            expense_date = date.fromisoformat(expense_date_str)
            amount = float(amount)
        except(ValueError, TypeError):
            return jsonify({'error': 'invalid amount or date format'}), 400

        new_expense = Expense(name=name,
                            amount=amount,
                            category=category,
                            expense_date=expense_date,
                            user_id=user_id
                            )

        db.session.add(new_expense)
        db.session.commit()
        return jsonify(new_expense.to_dict()), 201

    # UPDATE EXPENSE
    @app.route('/api/expenses/<int:expense_id>', methods=["PUT"])
    @jwt_required()
    def update_expense(expense_id):
        user_id = int(get_jwt_identity())
        expense = db.get_or_404(Expense, expense_id)

        if expense.user_id != user_id:
            return jsonify({'error': 'unauthorized'}), 403
        
        post_body = request.get_json()
        expense.name = post_body.get('name', expense.name)
        expense.amount = post_body.get('amount', expense.amount)
        expense.category = post_body.get('category', expense.category)

        if post_body.get('expense_date'):
            expense.expense_date = date.fromisoformat(post_body.get('expense_date'))

        db.session.commit()
        return jsonify(expense.to_dict()), 200

    # DELETE EXPENSE
    @app.route('/api/expenses/<int:expense_id>', methods=["DELETE"])
    @jwt_required()
    def delete_expense(expense_id):
        user_id = int(get_jwt_identity())
        expense = db.get_or_404(Expense, expense_id)

        if expense.user_id != user_id:
            return jsonify({'error': 'unauthorized'}), 403
        
        db.session.delete(expense)
        db.session.commit()

        return "", 204
    
    return app
    

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)