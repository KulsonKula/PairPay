from logging import getLogger
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Bill, User, Invitation, InvitationStatus
from app.services.bill_service import get_bills_for_user, update_bill_fields, get_bill_for_user, delete_bill, invite_user_to_bill
from app.utils.helpers import serialize_bill
from app import db
from http import HTTPStatus
from sqlalchemy.exc import SQLAlchemyError


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
        }), HTTPStatus.OK
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching bills for user {
                     current_user}: {str(e)}")
        return jsonify({"message": "Failed to fetch bills due to a database error"}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        logger.error(f"Error fetching bills for user {current_user}: {str(e)}")
        return jsonify({
            "message": "Failed to fetch user's bills",
            "message": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR


@bill_bp.route('/api/bills/<int:bill_id>', methods=['GET'])
@jwt_required()
def get_specific_bill(bill_id):
    current_user = get_jwt_identity()

    try:
        bill = get_bill_for_user(bill_id, current_user)

        if not bill:
            return jsonify({
                "message": "Bill not found or you do not have access to it"
            }), HTTPStatus.NOT_FOUND

        return jsonify({
            "bill": serialize_bill(bill)
        }), HTTPStatus.OK

    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving bill {
                     bill_id} for user {current_user}: {str(e)}")
        return jsonify({
            "message": "Failed to retrieve bill due to a database error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        logger.error(f"Unexpected error retrieving bill {
                     bill_id} for user {current_user}: {str(e)}")
        return jsonify({
            "message": "An unexpected error occurred"
        }), HTTPStatus.INTERNAL_SERVER_ERROR


@bill_bp.route('/api/create-bill', methods=['POST'])
@jwt_required()
def create_bill():
    current_user = get_jwt_identity()

    try:
        bill_data = request.get_json()

        if not bill_data:
            return jsonify({"message": "No input data provided"}), HTTPStatus.BAD_REQUEST

        bill = Bill(
            user_creator_id=current_user,
            name=bill_data.get("name"),
            label=bill_data.get("label"),
            status=bill_data.get("status"),
            total_sum=bill_data.get("total_sum")
        )

        db.session.add(bill)
        db.session.commit()

        logger.info(f"Bill created with ID {
                    bill.id} by user {current_user}")

        return jsonify({
            "message": "Bill created successfully",
            "bill": serialize_bill(bill)
        }), HTTPStatus.CREATED
    except SQLAlchemyError as e:
        logger.error(f"Database error creating bill for user {
                     current_user}: {str(e)}")
        return jsonify({"message": "Failed to create bill due to a database error"}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        logger.error(f"Error creating bill for user {
            current_user}: {str(e)}")
        return jsonify({
            "message": "Failed to create bill",
            "error": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR


@bill_bp.route('/api/bills/<int:bill_id>', methods=['PUT'])
@jwt_required()
def modify_specific_bill(bill_id):
    current_user = get_jwt_identity()

    try:
        bill_data = request.get_json()
        if not bill_data:
            return jsonify({"message": "No input data provided"}), HTTPStatus.BAD_REQUEST

        bill = Bill.query.filter_by(
            id=bill_id, user_creator_id=current_user).first()
        if not bill:
            logger.warning(f"Bill with ID {bill_id} not found or user {
                           current_user} is not the creator")
            return jsonify({"message": "Bill not found or you are not authorized to modify it"}), HTTPStatus.NOT_FOUND

        update_bill_fields(bill, bill_data)

        db.session.commit()

        logger.info(f"Bill with ID {bill.id} modified by user {current_user}")

        return jsonify({
            "message": "Bill updated successfully",
            "bill": serialize_bill(bill)
        }), HTTPStatus.OK

    except SQLAlchemyError as e:
        logger.error(f"Database error modifying bill {
                     bill_id} for user {current_user}: {str(e)}")
        return jsonify({"message": "Failed to modify the bill due to a database error"}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        logger.error(f"Unexpected error modifying bill {
                     bill_id} for user {current_user}: {str(e)}")
        return jsonify({"message": "An unexpected error occurred"}), HTTPStatus.INTERNAL_SERVER_ERROR


@bill_bp.route('/api/bills/<int:bill_id>', methods=['DELETE'])
@jwt_required()
def delete_specific_bill(bill_id):
    current_user = get_jwt_identity()
    try:
        bill = delete_bill(bill_id, current_user)

        return jsonify({"message": f"Bill {bill.id} deleted successfully"}), HTTPStatus.OK
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred while deleting bill {
                     bill_id}: {str(e)}")
        return jsonify({"message": "Database error occurred while deleting the bill"}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        logger.error(f"Unexpected error occurred while deleting bill {
                     bill_id}: {str(e)}")
        return jsonify({"message": "An unexpected error occurred"}), HTTPStatus.INTERNAL_SERVER_ERROR


@bill_bp.route('/api/bills/<int:bill_id>/invite', methods=['POST'])
@jwt_required()
def invite_to_bill(bill_id):
    current_user = get_jwt_identity()
    invite_data = request.get_json()

    try:
        invitee_id = invite_data.get("invitee_id")

        if not invitee_id:
            return jsonify({"message": "Invitee ID is required"}), HTTPStatus.BAD_REQUEST

        invitation = invite_user_to_bill(bill_id, current_user, invitee_id)
        return jsonify({"message": "Invitation sent successfully", "invitation_id": invitation.id}), HTTPStatus.CREATED

    except PermissionError as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except ValueError as e:
        return jsonify({"message": str(e)}), HTTPStatus.BAD_REQUEST
    except SQLAlchemyError as e:
        logger.error(f"Database error while sending invitation: {str(e)}")
        return jsonify({"message": "Database error occurred while processing the invitation"}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        logger.error(f"Error while sending invitation: {str(e)}")
        return jsonify({"message": "An unexpected error occurred"}), HTTPStatus.INTERNAL_SERVER_ERROR


@bill_bp.route('/api/invitations/<int:invitation_id>/accept', methods=['POST'])
@jwt_required()
def accept_invitation(invitation_id):
    current_user = get_jwt_identity()

    try:
        invitation = Invitation.query.filter_by(
            id=invitation_id, invitee_id=current_user, status=InvitationStatus.PENDING).first()
        if not invitation:
            return jsonify({"message": "Invitation not found or already handled"}), HTTPStatus.NOT_FOUND

        bill = Bill.query.get(invitation.bill_id)
        bill.users.append(User.query.get(current_user))

        invitation.status = InvitationStatus.ACCEPTED
        db.session.commit()

        return jsonify({"message": "Invitation accepted successfully"}), HTTPStatus.OK
    except Exception as e:
        logger.error(f"Error accepting invitation: {str(e)}")
        return jsonify({"message": "Failed to accept invitation"}), HTTPStatus.INTERNAL_SERVER_ERROR
