from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
from app.models import Friendship
from app import db
from app.models import InvitationStatus
from app.models.user import User
from app.services.debt_service import DebtService


class FriendshipService:
    def __init__(self, current_user):
        self.current_user = current_user
        self.debt_service = DebtService(current_user)

    def send_request(self, friend_email):
        try:
            friend = User.query.filter_by(mail=friend_email).first()

            if not friend:
                return {
                    "message": "No user found with the given email"
                }, HTTPStatus.NOT_FOUND

            if self.current_user == friend.id:
                return {
                    "message": "Error sending request to yourself"
                }, HTTPStatus.BAD_REQUEST

            friendship = Friendship.query.filter(
                (
                    (Friendship.user_id == self.current_user)
                    & (Friendship.friend_id == friend.id)
                )
                | (
                    (Friendship.user_id == friend.id)
                    & (Friendship.friend_id == self.current_user)
                )
            ).first()

            if friendship:
                if friendship.status == InvitationStatus.PENDING:
                    return {
                        "message": "Friend request already pending"
                    }, HTTPStatus.BAD_REQUEST
                elif friendship.status == InvitationStatus.ACCEPTED:
                    return {
                        "message": "You are already friends"
                    }, HTTPStatus.BAD_REQUEST
                elif friendship.status == InvitationStatus.DECLINED:
                    friendship.status = InvitationStatus.PENDING
                    db.session.commit()
                    return {
                        "message": "Friend request resent successfully"
                    }, HTTPStatus.OK

            new_friendship = Friendship(
                user_id=self.current_user,
                friend_id=friend.id,
                status=InvitationStatus.PENDING,
            )
            db.session.add(new_friendship)
            db.session.commit()
            return {"message": "Friend request sent successfully"}, HTTPStatus.CREATED

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def accept_request(self, request_id):
        try:
            friendship = Friendship.query.get(request_id)

            if not friendship or friendship.friend_id != self.current_user:
                return {"message": "Friend request not found"}, HTTPStatus.NOT_FOUND

            friendship.status = InvitationStatus.ACCEPTED
            db.session.commit()
            return {"message": "Friend request accepted"}, HTTPStatus.OK

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def decline_request(self, request_id):
        try:
            friendship = Friendship.query.get(request_id)

            if not friendship or friendship.friend_id != self.current_user:
                return {"message": "Friend request not found"}, HTTPStatus.NOT_FOUND

            friendship.status = InvitationStatus.DECLINED
            db.session.commit()
            return {"message": "Friend request declined"}, HTTPStatus.OK

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_friends(self):
        try:
            friends = (
                db.session.query(User)
                .join(
                    Friendship,
                    db.or_(
                        db.and_(
                            Friendship.friend_id == User.id,
                            Friendship.user_id == self.current_user,
                            Friendship.status == InvitationStatus.ACCEPTED,
                        ),
                        db.and_(
                            Friendship.user_id == User.id,
                            Friendship.friend_id == self.current_user,
                            Friendship.status == InvitationStatus.ACCEPTED,
                        ),
                    ),
                )
                .all()
            )

            friend_list = []
            debt_service = DebtService(self.current_user)

            for friend in friends:
                debt_info = debt_service.get_debt_with_friend(friend.id)
                friend_data = {
                    "id": friend.id,
                    "mail": friend.mail,
                    "debt_info": debt_info,
                }
                friend_list.append(friend_data)

            return {"friends": friend_list}, HTTPStatus.OK

        except SQLAlchemyError as e:
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_pending_requests(self):
        try:
            pending_requests = Friendship.query.filter_by(
                friend_id=self.current_user, status=InvitationStatus.PENDING
            ).all()

            request_list = [
                {
                    "id": request.id,
                    "user_id": request.user_id,
                    "mail": request.user.mail,
                }
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
