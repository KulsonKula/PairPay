from logging import getLogger
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from app.services.friendship_service import (
    accept_request_service,
    decline_request_service,
    send_request_service,
    get_pending_requests_service,
    get_friends_service,
)

friend_bp = Blueprint("friend_bp", __name__)
logger = getLogger(__name__)


@friend_bp.route("/send_request", methods=["POST"], endpoint="send_friend_request")
@jwt_required()
def send_friend_request():
    try:
        current_user_id = get_jwt_identity()
        friend_id = request.json.get("friend_id")

        if not friend_id:
            return jsonify({"message": "Friend ID is required"}), HTTPStatus.BAD_REQUEST

        response, status_code = send_request_service(current_user_id, friend_id)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@friend_bp.route(
    "/accept_request/<int:request_id>",
    methods=["POST"],
    endpoint="accept_friend_request",
)
@jwt_required()
def accept_friend_request(request_id):
    try:
        current_user = get_jwt_identity()
        response, status_code = accept_request_service(current_user, request_id)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@friend_bp.route(
    "/decline_request/<int:request_id>",
    methods=["POST"],
    endpoint="decline_friend_request",
)
@jwt_required()
def decline_friend_request(request_id):
    try:
        current_user = get_jwt_identity()
        response, status_code = decline_request_service(current_user, request_id)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@friend_bp.route("/friends", methods=["GET"], endpoint="get_friends")
@jwt_required()
def get_friends():
    try:
        current_user = get_jwt_identity()
        response, status_code = get_friends_service(current_user)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify({"message": "Unexpected error occurred", "details": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@friend_bp.route("pending_requests", methods=["GET"], endpoint="get_pending_requests")
@jwt_required()
def get_pending_requests():
    try:
        current_user_id = get_jwt_identity()
        response, status_code = get_pending_requests_service(current_user_id)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"message": "Unexpected error occurred", "details": str(e)}), 500
