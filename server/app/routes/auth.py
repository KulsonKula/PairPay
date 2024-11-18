from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    surname = data.get('surname')
    mail = data.get('mail')
    password = data.get('password')

    if not all([name, surname, mail, password]):
        return jsonify({"msg": "All fields (name, surname, mail, password) are required"}), 400

    try:
        user_exists = User.query.filter_by(mail=mail).first()
        if user_exists:
            return jsonify({"msg": "A user with this email address already exists"}), 400

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            surname=surname,
            mail=mail,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User successfully registered"}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(message="An error occurred during user registration.", error=str(e)), 500


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    mail = data.get("mail")
    password = data.get("password")

    user = User.query.filter_by(mail=mail).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    return jsonify({"message": "Invalid E-mail or prassword"}), 401


@auth_bp.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
