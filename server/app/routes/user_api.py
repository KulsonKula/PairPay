from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, Blueprint
from app.models import User
from http import HTTPStatus

user_bp = Blueprint('user_bp', __name__)


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
