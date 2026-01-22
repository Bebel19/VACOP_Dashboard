from flask import Blueprint, request, jsonify
from backend.models import User
from backend.extensions import db, bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Nom d'utilisateur et mot de passe requis"}), 400

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(
            identity=user.id,
            additional_claims={"role": user.role, "username": user.username},
            expires_delta=timedelta(days=1)
        )
        return jsonify({
            "access_token": access_token,
            "role": user.role,
            "username": user.username
        }), 200
    
    return jsonify({"msg": "Identifiants invalides"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Nom d'utilisateur et mot de passe requis"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Nom d'utilisateur déjà pris"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password_hash=hashed_pw, role='user')
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "Utilisateur créé avec succès"}), 201