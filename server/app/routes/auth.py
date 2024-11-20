from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from logging import getLogger
from http import HTTPStatus
from flask_jwt_extended import get_jwt
from app.models import *
from datetime import datetime, timezone

auth_bp = Blueprint('auth_bp', __name__)

logger = getLogger(__name__)


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    surname = data.get('surname')
    mail = data.get('mail')
    password = data.get('password')

    if not all([name, surname, mail, password]):
        return jsonify({"msg": "All fields (name, surname, mail, password) are required"}), HTTPStatus.BAD_REQUEST

    try:
        user_exists = User.query.filter_by(mail=mail).first()
        if user_exists:
            return jsonify({"msg": "A user with this email address already exists"}), HTTPStatus.BAD_REQUEST

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            surname=surname,
            mail=mail,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User successfully registered"}), HTTPStatus.CREATED

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(message="An error occurred during user registration.", error=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    mail = data.get("mail")
    password = data.get("password")

    user = User.query.filter_by(mail=mail).first()

    if user and check_password_hash(user.password, password):
        logger.info(user.id)
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token), HTTPStatus.OK

    return jsonify({"message": "Invalid E-mail or prassword"}), HTTPStatus.UNAUTHORIZED


@auth_bp.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token)


@auth_bp.route('/api/logout', methods=['DELETE'])
@jwt_required()
def blacklist_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(msg="JWT revoked")
