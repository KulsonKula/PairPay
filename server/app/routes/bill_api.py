from logging import getLogger
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.bill_service import get_bills_for_user

bill_bp = Blueprint('bill_bp', __name__)
logger = getLogger(__name__)


@bill_bp.route('/api/bills', methods=['GET'])
@jwt_required()
def get_all_bills():
    current_user = get_jwt_identity()

    try:
        bills = get_bills_for_user(current_user)

        bills_data = [bill.to_dict() for bill in bills]
        logger.info(f"Bills data: {bills_data}")

        return jsonify({
            "bills": bills_data
        }), 200
    except Exception as e:
        logger.error(f"Error fetching bills for user {current_user}: {str(e)}")
        return jsonify({
            "message": str(e)
        }), 500
