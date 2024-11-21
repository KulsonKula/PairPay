from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, Blueprint, request
from app.models import User
from http import HTTPStatus
from app import db
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user_bp', __name__)

# CREATE USER IN auth.py


@user_bp.route('/api/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()

        user = User.query.get(current_user_id)

        if user:
            return jsonify(user.to_dict()), HTTPStatus.OK
        else:
            return jsonify({
                "message": "User not found"
            }), HTTPStatus.NOT_FOUND

    except Exception as e:
        return jsonify({
            "message": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR


@user_bp.route('/api/del_user', methods=['DELETE'])
@jwt_required()
def del_user():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        del_user_id = data.get("del_user_id")

        if not del_user_id:
            return jsonify({"error": "del_user_id is required."}), 400

        user = User.query.get(current_user_id)
        del_user = User.query.get(del_user_id)

        if not del_user:
            return jsonify({"error": "User not found."}), 404

        if del_user == user or user.admin:
            db.session.delete(del_user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully."}), 200
        else:
            return jsonify({"error": "Unauthorized action."}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/api/update_user', methods=['POST'])
@jwt_required()
def update_user():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        name = data.get("name")
        mail = data.get("mail")
        surname = data.get("surname")
        password = data.get("password")
        updated_user_id = data.get("updated_user_id")

        if not updated_user_id:
            return jsonify({"error": "updated_user_id is required."}), 400

        user = User.query.get(current_user_id)
        updated_user = User.query.get(updated_user_id)

        if not updated_user:
            return jsonify({"error": "User not found."}), 404

        if updated_user == user or user.admin:
            if name:
                updated_user.name = name
            if mail:
                updated_user.mail = mail
            if surname:
                updated_user.surname = surname
            if password:
                updated_user.password = generate_password_hash(password)

                db.session.commit()
            return jsonify({"message": "User updated successfully."}), 200
        else:
            return jsonify({"error": "Unauthorized action."}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/api/make_admin_user', methods=['POST'])
@jwt_required()
def make_admin_user():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        make_admin_user_id = data.get("make_admin_user_id")

        if not make_admin_user_id:
            return jsonify({"error": "make_admin_user_id is required."}), 400

        user = User.query.get(current_user_id)
        make_admin_user = User.query.get(make_admin_user_id)

        if not make_admin_user:
            return jsonify({"error": "User not found."}), 404

        if user.admin:
            make_admin_user.admin = True
            db.session.commit()
            return jsonify({"message": "User have granted admin successfully."}), 200
        else:
            return jsonify({"error": "Unauthorized action."}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500
