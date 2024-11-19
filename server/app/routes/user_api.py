from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, Blueprint
from app.models import User

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/api/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()

        user = User.query.get(current_user_id)

        if user:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({
                "message": "User not found"
            }), 404

    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500
