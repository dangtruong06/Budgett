from flask import Flask, jsonify, request
from extensions import db
from config import Config
from flask_migrate import Migrate
from models import User, Expense
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import date
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app,db)
jwt = JWTManager(app)
CORS(app)

@app.route('/')
def index(): 
    return jsonify({'message': 'Budgett API running!'})

@app.route('/api/register', methods=["POST"])
def register():
    response = request.get_json()
    email = response.get('email')
    password = response.get('password')

    #validate unique email
    email_exists = db.session.execute(db.select(User).where(User.email == email)).scalar()
    if email_exists:
        return jsonify({'error': 'resource already exists'}), 409
    
    # hash password, create new user
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(email=email, password_hash=password_hash.decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'success': 'new user created'}), 201
    
@app.route('/api/login', methods=["POST"])
def login():
    response = request.get_json()
    input_email = response.get('email')
    input_password = response.get('password').encode('utf-8')

    user = db.session.execute(db.select(User).where(User.email == input_email)).scalar()

    if user and bcrypt.checkpw(input_password, user.password_hash.encode('utf-8')):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'unauthorized'}), 401

# LOGIN REQUIRED ROUTES
    
# GET EXPENSES
@app.route('/api/expenses', methods=["GET"])
@jwt_required()
def get_expense():
    user_id = int(get_jwt_identity())
    expenses = db.session.execute(db.select(Expense).where(Expense.user_id == user_id)).scalars().all()

    return jsonify([expense.to_dict() for expense in expenses]), 200

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
        return jsonify({'error': 'unauthorize'}), 403
    
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
        return jsonify({'error': 'unauthorize'}), 403
    
    db.session.delete(expense)
    db.session.commit()

    return "", 204

if __name__ == '__main__':
    app.run(debug=True, port=5001)