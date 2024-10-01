from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, jwt_required
from models import db, User, Expense
from utils import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
jwt.init_app(app)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully."}), 201

@app.route('/login', methods=['POST'])
def login():
    