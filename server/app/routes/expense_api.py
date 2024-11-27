from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.expense_service import ExpenseService
from http import HTTPStatus

expense_bp = Blueprint("expense_bp", __name__)


@expense_bp.route("/bill/<int:bill_id>/expenses", methods=["GET"])
@jwt_required()
def get_all_expenses(bill_id):
    try:
        current_user = get_jwt_identity()
        expense_service = ExpenseService(current_user)
        response, status_code = expense_service.get_expenses(bill_id)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@expense_bp.route("/bill/<int:bill_id>/expenses/<int:expense_id>", methods=["GET"])
@jwt_required()
def get_specific_expense(bill_id, expense_id):
    try:
        current_user = get_jwt_identity()
        expense_service = ExpenseService(current_user)
        response, status_code = expense_service.get_specifc_expense(expense_id, bill_id)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@expense_bp.route("/bill/<int:bill_id>/expense/create", methods=["POST"])
@jwt_required()
def create_new_expense(bill_id):
    try:
        current_user = get_jwt_identity()
        expense_service = ExpenseService(current_user)
        expense_data = request.get_json()
        response, status_code = expense_service.create_expense(bill_id, expense_data)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@expense_bp.route("/bill/expense/<int:expense_id>", methods=["PUT"])
@jwt_required()
def modify_expense(expense_id):
    try:
        current_user = get_jwt_identity()
        expense_service = ExpenseService(current_user)
        expense_data = request.get_json()
        response, status_code = expense_service.modify_expense(expense_id, expense_data)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@expense_bp.route("/bill/expense/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    try:
        current_user = get_jwt_identity()
        expense_service = ExpenseService(current_user)
        response, status_code = expense_service.delete_expense(expense_id)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
