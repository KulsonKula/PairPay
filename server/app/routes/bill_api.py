from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from app.services.bill_service import BillSerivce

bill_bp = Blueprint("bill_bp", __name__)


@bill_bp.route("/bills/created", methods=["GET"])
@jwt_required()
def get_all_bills_created():
    try:
        current_user = get_jwt_identity()
        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.get_created_bills()
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
        response, status_code = bill_service.get_assigned_bills()
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


@bill_bp.route("/bills/<int:bill_id>/invite", methods=["POST"])
@jwt_required()
def invite_to_bill(bill_id):
    try:
        current_user = get_jwt_identity()
        invite_data = request.get_json()

        if not invite_data or "invitee_id" not in invite_data:
            return (
                jsonify({"message": "Invitee ID is required"}),
                HTTPStatus.BAD_REQUEST,
            )

        invitee_id = invite_data.get("invitee_id")
        bill_service = BillSerivce(current_user)
        response, status_code = bill_service.invite_to_bill(
            bill_id, invitee_id)
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
