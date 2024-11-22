from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
from app.models import Friendship
from app import db
from app.models import InvitationStatus


def send_request_service(current_user, friend_id):
    try:
        if current_user == friend_id:
            return {
                "message": "error sending request to yourself"
            }, HTTPStatus.BAD_REQUEST

        friendship = Friendship.query.filter(
            ((Friendship.user_id == current_user) & (Friendship.friend_id == friend_id))
            | (
                (Friendship.user_id == friend_id)
                & (Friendship.friend_id == current_user)
            )
        ).first()

        if friendship:
            return {"message": "Request already exist"}, HTTPStatus.BAD_REQUEST

        new_friendship = Friendship(user_id=current_user, friend_id=friend_id)
        db.session.add(new_friendship)
        db.session.commit()
        return {"message": "Friend request sent successfully"}, HTTPStatus.CREATED
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"message": f"Database error {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        return {
            "message": f"An unexpected error occured ${str(e)}"
        }, HTTPStatus.INTERNAL_SERVER_ERROR


def accept_request_service(current_user, request_id):
    try:
        friendship = Friendship.query.get(request_id)

        if not friendship or friendship.friend_id != current_user:
            return {"message": "Friend request not found"}, HTTPStatus.NOT_FOUND

        friendship.status = InvitationStatus.ACCEPTED
        db.session.commit()
        return {"message": "Friend request accepetd"}, HTTPStatus.OK
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"message": f"Database error {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        return {
            "message": f"An unexpected error occured ${str(e)}"
        }, HTTPStatus.INTERNAL_SERVER_ERROR


def decline_request_service(current_user, request_id):
    try:
        friendship = Friendship.query.get(request_id)

        if not friendship or friendship.friend_id != current_user:
            return {"message": "Friend request not found"}, HTTPStatus.NOT_FOUND

        friendship.status = InvitationStatus.DECLINED
        db.session.commit()
        return {"message": "Friend request accepetd"}, HTTPStatus.OK
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"message": f"Database error {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        return {
            "message": f"An unexpected error occured ${str(e)}"
        }, HTTPStatus.INTERNAL_SERVER_ERROR


def get_friends_service(current_user):
    try:
        friends_query = Friendship.query.filter(
            (Friendship.user_id == current_user)
            | (Friendship.friend_id == current_user),
            Friendship.status == InvitationStatus.ACCEPTED,
        ).all()

        friends = [
            {
                "id": (
                    friendship.friend.id
                    if friendship.user_id == current_user
                    else friendship.user.id
                ),
                "mail": (
                    friendship.friend.mail
                    if friendship.user_id == current_user
                    else friendship.user.mail
                ),
            }
            for friendship in friends_query
        ]
        return {"friends": friends}, HTTPStatus.OK
    except SQLAlchemyError as e:
        return {
            "message": "Database error",
            "details": str(e),
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        return {
            "message": "Unexpected error occurred",
            "details": str(e),
        }, HTTPStatus.INTERNAL_SERVER_ERROR


def get_pending_requests_service(current_user_id):
    try:
        pending_requests = Friendship.query.filter_by(
            friend_id=current_user_id, status="pending"
        ).all()

        request_list = [
            {"id": request.id, "user_id": request.user_id, "mail": request.user.mail}
            for request in pending_requests
        ]
        return {"pending_requests": request_list}, HTTPStatus.OK
    except SQLAlchemyError as e:
        return {
            "message": "Database error",
            "details": str(e),
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        return {
            "message": "Unexpected error occurred",
            "details": str(e),
        }, HTTPStatus.INTERNAL_SERVER_ERROR
