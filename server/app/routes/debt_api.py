from http import HTTPStatus
from logging import getLogger
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.debt_service import DebtService


debt_bp = Blueprint("debt", __name__, url_prefix="/api/debt")

logger = getLogger(__name__)


@debt_bp.route("/balances", methods=["GET"])
@jwt_required()
def get_debt_balances():
    try:
        current_user = get_jwt_identity()

        debt_service = DebtService(current_user)
        response, status_code = debt_service.get_user_balances()
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
