from flask import Flask, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, jwt_required
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
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token), 200
    
@app.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    filters = request.args
    query = Expense.query.filter_by(user_id=user_id)
    
    if 'start_date' in filters and 'end_date' in filters:
        start_date = datetime.fromisoformat(filters['start_date'])
        end_date = datetime.fromisoformat(filters['end_date'])
        query = query.filter(Expense.date.between(start_date, end_date))
        
    if 'category' in filters:
        query = query.filter_by(category=filters['category'])
        
    expenses = query.all()
    return jsonify([{'id': exp.id, 'category': exp.category, 'amount': exp.amount, 'date': exp.date} for exp in expenses]), 200

@app.route('/expense', methods=['POST'])
@jwt_required()
def add_expense():
    user_id = get_jwt_identity()    
    data = request.json
    new_expense = Expense(
        category=data['category'], 
        amount=data['amount'],
        user_id=user_id
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully"}), 201

@app.route('/expenses/<int:expense_id', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    user_id = get_jwt_identity()
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != user_id:
        return jsonify ({"message": "Unauthorized"}), 403
    db.session.delete(expense)
    db.session.commit()
    return jsonify ({"message": "Expense deleted."}), 200

@app.route('/expense/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    user_id = get_jwt_identity()
    data = request.json
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != user_id:
        return jsonify({"message": "Unauthorized."}), 403
    expense.category = data['category']
    expense.amount = data['amount']
    db.session.commit()
    return jsonify({"message": "Expense updated."}), 200