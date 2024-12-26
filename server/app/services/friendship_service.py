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

    def send_request(self, friend_id):
        try:
            if self.current_user == friend_id:
                return {
                    "message": "Error sending request to yourself"
                }, HTTPStatus.BAD_REQUEST

            friendship = Friendship.query.filter(
                (
                    (Friendship.user_id == self.current_user)
                    & (Friendship.friend_id == friend_id)
                )
                | (
                    (Friendship.user_id == friend_id)
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
                friend_id=friend_id,
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
            friends_query = (
                db.session.query(User)
                .join(
                    Friendship,
                    (
                        (Friendship.friend_id == User.id)
                        & (Friendship.user_id == self.current_user)
                    )
                    | (
                        (Friendship.user_id == User.id)
                        & (Friendship.friend_id == self.current_user)
                    ),
                )
                .filter(Friendship.status == InvitationStatus.ACCEPTED)
                .all()
            )

            # Debugowanie
            print("Friends query result:", friends_query)
            friend_list = []
            for friend in friends_query:
                try:
                    print(f"Friend object: {friend}, ID: {friend.id}")
                    debt_info = self.debt_service.get_debt_with_friend(friend.id)
                    print(f"Debt info: {debt_info}")

                    friend_data = {
                        "id": friend.id,
                        "mail": friend.mail,
                        "debt_info": debt_info,
                    }
                    friend_list.append(friend_data)
                except Exception as e:
                    print(
                        f"Error processing friend {friend.id if hasattr(friend, 'id') else friend}: {e}"
                    )
                    raise e

            return {"friends": friend_list}, HTTPStatus.OK

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
