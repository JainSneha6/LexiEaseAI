from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from extensions import db  

auth_bp = Blueprint('auth', __name__)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    test_score = db.Column(db.Integer, default=0)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify(message='User already exists!'), 409

    new_user = User(email=data['email'], password=generate_password_hash(data['password'], method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message='User created successfully!'), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(message='Login successful!', access_token=access_token), 200
    return jsonify(message='Invalid email or password!'), 401
