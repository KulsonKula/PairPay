from logging import getLogger
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from sqlalchemy.exc import SQLAlchemyError
from ..utils.helpers import make_log_wrapper
from app.services.bill_service import BillSerivce

bill_bp = Blueprint("bill_bp", __name__)

logger = getLogger(__name__)


@bill_bp.route("/bills/created", methods=["GET"])
@jwt_required()
def get_all_bills_created():
    try:
        current_user = get_jwt_identity()
        logger.info(f"Test200: {current_user}")

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 4, type=int)

        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.get_created_bills(page, per_page)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/bills/assigned", methods=["GET"])
@jwt_required()
def get_all_bills_assigned():
    try:
        current_user = get_jwt_identity()
        bill_service = BillSerivce(current_user)

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 4, type=int)

        response, status_code = bill_service.get_assigned_bills(page, per_page)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/bills/<int:bill_id>", methods=["GET"])
@jwt_required()
def get_specific_bill(bill_id):
    try:
        current_user = get_jwt_identity()
        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.get_specific_bill(bill_id)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/create-bill", methods=["POST"])
@jwt_required()
@make_log_wrapper
def create_bill():
    try:
        current_user = get_jwt_identity()
        bill_data = request.get_json()

        if not bill_data:
            return (
                jsonify({"message": "No input data provided"}),
                HTTPStatus.BAD_REQUEST,
            )

        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.create_bill(bill_data)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/bills/<int:bill_id>", methods=["PUT"])
@jwt_required()
@make_log_wrapper
def modify_specific_bill(bill_id):
    try:
        current_user = get_jwt_identity()
        bill_data = request.get_json()

        if not bill_data:
            return (
                jsonify({"message": "No input data provided"}),
                HTTPStatus.BAD_REQUEST,
            )

        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.modify_bill(bill_id, bill_data)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/bills/<int:bill_id>", methods=["DELETE"])
@jwt_required()
@make_log_wrapper
def delete_specific_bill(bill_id):
    try:
        current_user = get_jwt_identity()
        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.delete_bill(bill_id)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/bills/<int:bill_id>/invite-user", methods=["POST"])
@jwt_required()
@make_log_wrapper
def invite_to_bill(bill_id):
    try:
        current_user = get_jwt_identity()
        invite_data = request.get_json()

        if not invite_data or "user_email" not in invite_data:
            return (
                jsonify({"message": "User Email is required"}),
                HTTPStatus.BAD_REQUEST,
            )

        user_email = invite_data.get("user_email")
        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.invite_user_to_bill(bill_id, user_email)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/bills/<int:bill_id>/invite-users", methods=["POST"])
@jwt_required()
@make_log_wrapper
def invite_users_to_bill(bill_id):
    try:
        current_user = get_jwt_identity()

        invite_data = request.get_json()

        if not invite_data or "user_emails" not in invite_data:
            return (
                jsonify({"message": "User Emails are required"}),
                HTTPStatus.BAD_REQUEST,
            )

        user_emails = invite_data["user_emails"]

        if not isinstance(user_emails, list) or not user_emails:
            return (
                jsonify({"message": "A list of user emails is required"}),
                HTTPStatus.BAD_REQUEST,
            )

        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.invite_users_to_bill(bill_id, user_emails)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/invitations/<int:invitation_id>/accept", methods=["POST"])
@jwt_required()
def accept_invitation(invitation_id):
    try:
        current_user = get_jwt_identity()
        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.accept_invitation(invitation_id)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/invitations/<int:invitation_id>/decline", methods=["POST"])
@jwt_required()
def decline_invitation(invitation_id):
    try:
        current_user = get_jwt_identity()
        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.decline_invitation(invitation_id)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/invitations", methods=["GET"])
@jwt_required()
def get_user_invitations():
    try:
        current_user = get_jwt_identity()
        logger.info(f"Fetching invitations for user: {current_user}")

        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.get_user_inviations()

        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/bills/<int:bill_id>/available-friends", methods=["GET"])
@jwt_required()
def get_friends_not_in_bill(bill_id):
    try:
        current_user = get_jwt_identity()
        logger.info(
            f"Fetching available friends for bill {bill_id} and user {current_user}"
        )

        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.get_friends_not_in_bill(bill_id)

        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/bills/<int:bill_id>/participants", methods=["GET"])
@jwt_required()
def get_bill_users(bill_id):
    try:
        current_user = get_jwt_identity()
        logger.info(f"Fetching users for bill {bill_id}")

        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.get_bill_users(bill_id)

        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@bill_bp.route("/bills/<int:bill_id>/participant/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_participant_from_bill(bill_id, user_id):
    try:
        current_user = get_jwt_identity()

        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.delete_participant_from_bill(
            bill_id, user_id
        )

        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
