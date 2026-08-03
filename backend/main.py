from flask import Flask, jsonify, request
from extensions import db
from config import Config
from flask_migrate import Migrate
from models import User, Expense
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app,db)
jwt = JWTManager(app)

@app.route('/')
def index(): 
    return jsonify({'message': 'Budgett API running meow!'})

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
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'unauthorized'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5001)