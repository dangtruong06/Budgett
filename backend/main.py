from flask import Flask, jsonify
from extensions import db
from config import Config
from flask_migrate import Migrate
from models import User, Expense

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app,db)

@app.route('/')
def index(): 
    return jsonify({'message': 'Budgett API running meow!'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)