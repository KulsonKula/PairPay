from logging import getLogger

from app.models import User, Bill, bill_user, Invitation, InvitationStatus, Expense
from app import db
from http import HTTPStatus
from sqlalchemy.exc import SQLAlchemyError

logger = getLogger(__name__)


class BillSerivce:
    def __init__(self, current_user):
        self.current_user = current_user

    def get_created_bills(self, page=1, per_page=5):
        try:
            bills = Bill.query.filter_by(user_creator_id=self.current_user).paginate(
                page=page, per_page=per_page, error_out=False
            )
            bills_data = [bill.to_dict() for bill in bills.items]
            return {
                "bills": bills_data,
                "total_items": bills.total,
                "total_pages": bills.pages,
                "current_page": bills.page,
            }, HTTPStatus.OK
        except SQLAlchemyError as e:
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_assigned_bills(self, page=1, per_page=5):
        try:
            bills = (
                Bill.query.outerjoin(bill_user)
                .filter(bill_user.c.user_id == self.current_user)
                .distinct()
                .paginate(page=page, per_page=per_page, error_out=False)
            )
            bills_data = [bill.to_dict() for bill in bills.items]
            return {
                "bills": bills_data,
                "total_items": bills.total,
                "total_pages": bills.pages,
                "current_page": bills.page,
            }, HTTPStatus.OK
        except SQLAlchemyError as e:
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_specific_bill(self, bill_id):
        try:
            bill = Bill.query.get(bill_id)

            if not bill:
                return (
                    {"message": "Bill not found or you do not have access to it"},
                    HTTPStatus.NOT_FOUND,
                )

            return {"bill": bill.to_dict()}, HTTPStatus.OK
        except SQLAlchemyError as e:
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def create_bill(self, bill_data):
        try:
            bill = Bill(
                user_creator_id=self.current_user,
                name=bill_data.get("name"),
                label=bill_data.get("label"),
                status=bill_data.get("status"),
            )

            db.session.add(bill)
            db.session.commit()
            logger.info(f"Bill created with ID {bill.id} by user {self.current_user}")
            return (
                {
                    "bill": bill.to_dict(),
                },
                HTTPStatus.CREATED,
            )
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def modify_bill(self, bill_id, bill_data):
        try:
            bill = Bill.query.filter_by(
                id=bill_id, user_creator_id=self.current_user
            ).first()

            if not bill:
                logger.warning(
                    f"Bill with ID {bill_id} not found or user {    self.current_user} is not the creator"
                )
                return (
                    {
                        "message": "Bill not found or you are not authorized to modify it"
                    },
                    HTTPStatus.NOT_FOUND,
                )

            self._update_bill_fields(bill, bill_data)
            db.session.commit()
            logger.info(f"Bill with ID {bill.id} modified by user {self.current_user}")
            return (
                {"bill": bill.to_dict()},
                HTTPStatus.OK,
            )
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def delete_bill(self, bill_id):
        try:
            bill = Bill.query.filter_by(
                id=bill_id, user_creator_id=self.current_user
            ).first()

            if not bill:
                return (
                    {"message": "Bill not found"},
                    HTTPStatus.NOT_FOUND,
                )

            db.session.delete(bill)
            db.session.commit()
            return (
                {"message": f"Bill {bill.id} deleted successfully"},
                HTTPStatus.OK,
            )
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def invite_to_bill(self, bill_id, invitee_id):
        try:
            if not invitee_id:
                return (
                    {"message": "Invitee ID is required"},
                    HTTPStatus.BAD_REQUEST,
                )

            bill = Bill.query.filter_by(
                id=bill_id, user_creator_id=self.current_user
            ).first()

            if not bill:
                return (
                    {"message": "Only creator of the bill can invite users"},
                    HTTPStatus.FORBIDDEN,
                )
            if any(user.id == invitee_id for user in bill.users):
                return (
                    {"message": "User is already part of the bill"},
                    HTTPStatus.BAD_REQUEST,
                )

            invitation = Invitation(
                inviter_id=self.current_user, invitee_id=invitee_id, bill_id=bill_id
            )
            db.session.add(invitation)
            db.session.commit()

            return (
                {
                    "message": "Invitation sent successfully",
                    "invitation_id": invitation.id,
                },
                HTTPStatus.CREATED,
            )
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def accept_invitation(self, invitation_id):
        try:
            invitation = Invitation.query.filter_by(
                id=invitation_id,
                invitee_id=self.current_user,
                status=InvitationStatus.PENDING,
            ).first()

            if not invitation:
                return (
                    {"message": "Invitation not found or already handled"},
                    HTTPStatus.NOT_FOUND,
                )

            bill = Bill.query.get(invitation.bill_id)
            bill.users.append(User.query.get(self.current_user))

            invitation.status = InvitationStatus.ACCEPTED
            db.session.commit()

            return {"message": "Invitation acceppted"}, HTTPStatus.OK
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def decline_invitation(self, invitation_id):
        try:
            invitation = Invitation.query.filter_by(
                id=invitation_id,
                invitee_id=self.current_user,
                status=InvitationStatus.PENDING,
            ).first()

            if not invitation:
                return (
                    {"message": "Invitation not found or already handled"},
                    HTTPStatus.NOT_FOUND,
                )

            bill = Bill.query.get(invitation.bill_id)
            bill.users.append(User.query.get(self.current_user))

            invitation.status = InvitationStatus.DECLINED
            db.session.commit()

            return {"message": "Invitation declined"}, HTTPStatus.OK
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def _update_bill_fields(self, bill, bill_data):
        updatable_fields = ["name", "label", "status"]
        for field in updatable_fields:
            if field in bill_data:
                setattr(bill, field, bill_data[field])
        self.calc_total_sum(bill.id)

    def calc_total_sum(bill_id):
        expenses = Expense.query.filter_by(bill_id=bill_id).all()
        return sum(exp.price for exp in expenses if exp.price is not None)
