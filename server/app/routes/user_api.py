from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, Blueprint, request
from app.models import User
from app.services.user_service import update_user_fields
from http import HTTPStatus
from app import db
from http import HTTPStatus
from ..utils.helpers import make_log_wrapper

user_bp = Blueprint("user_bp", __name__)

# CREATE USER IN auth.py
# PASSWORD RESET IN auth.py


@user_bp.route("/api/current_user", methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()

        user = User.query.get(current_user_id)

        if user:
            return jsonify(user.to_dict()), HTTPStatus.OK
        else:
            return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND

    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@user_bp.route("/api/user/del_user", methods=["DELETE"])
@jwt_required()
@make_log_wrapper
def del_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully."}), HTTPStatus.OK

    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@user_bp.route("/api/user/update", methods=["PUT"])
@jwt_required()
@make_log_wrapper
def update_user():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND

        update_user_fields(user, data)
        db.session.commit()
        return jsonify({"message": "User updated successfully."}), HTTPStatus.OK

    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@user_bp.route("/api/user/admin/make_admin", methods=["POST"])
@jwt_required()
@make_log_wrapper
def make_admin():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user.admin:
            return jsonify({"error": "Unauthorized action."}), HTTPStatus.UNAUTHORIZED

        data = request.get_json()
        target_user = if_user_exist(data.get("target_user_id"))

        target_user.admin = True
        db.session.commit()
        return (
            jsonify({"message": "User granted admin privileges successfully."}),
            HTTPStatus.OK,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@user_bp.route("/api/user/admin/update", methods=["POST"])
@jwt_required()
@make_log_wrapper
def update_user_by_admin():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user.admin:
            return jsonify({"error": "Unauthorized action."}), HTTPStatus.UNAUTHORIZED

        data = request.get_json()
        target_user = if_user_exist(data.get("target_user_id"))

        update_user_fields(target_user, data)
        db.session.commit()
        return (
            jsonify({"message": "User granted admin privileges successfully."}),
            HTTPStatus.OK,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


def if_user_exist(user_id):

    if not user_id:
        return jsonify({"error": "user_id is required."}), HTTPStatus.BAD_REQUEST

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), HTTPStatus.NOT_FOUND

    return user
