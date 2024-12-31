from logging import getLogger
from app import db
from app.models import Expense, Bill, ExpenseParticipant, Debt
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
from app.services.bill_service import BillSerivce

logger = getLogger(__name__)


class ExpenseService:
    def __init__(self, current_user):
        self.current_user = current_user
        self.bill_service = BillSerivce(current_user)

    def get_expenses(self, bill_id):
        try:
            bill = Bill.query.get(bill_id)
            if not bill:
                return {"message": "Bill not found"}, HTTPStatus.NOT_FOUND

            if not self._is_user_participant(bill):
                return {
                    "message": "User is not a participant of the bill"
                }, HTTPStatus.FORBIDDEN

            expenses = Expense.query.filter_by(bill_id=bill_id).all()
            return {
                "expenses": [expense.to_dict() for expense in expenses]
            }, HTTPStatus.OK
        except SQLAlchemyError as e:
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_specifc_expense(self, expense_id, bill_id):
        try:
            bill = Bill.query.get(bill_id)
            if not bill:
                return {"message": "Bill not found"}, HTTPStatus.NOT_FOUND

            if not self._is_user_participant(bill):
                return {
                    "message": "User is not a participant of the bill"
                }, HTTPStatus.FORBIDDEN

            expense = Expense.query.filter_by(id=expense_id, bill_id=bill_id).first()
            if not expense:
                return {"message": "Expense not found"}, HTTPStatus.NOT_FOUND

            return {"expense": expense.to_dict()}, HTTPStatus.OK
        except SQLAlchemyError as e:
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def create_expense(self, bill_id, expense_data):
        try:
            bill = Bill.query.get(bill_id)
            if not bill:
                return {"message": "Bill not found"}, HTTPStatus.NOT_FOUND

            if not self._is_user_participant(bill):
                return {
                    "message": "User is not a participant of the bill"
                }, HTTPStatus.FORBIDDEN

            required_fields = ["name", "currency", "price", "payer"]
            for field in required_fields:
                if field not in expense_data:
                    return {
                        "message": f"Missing required field: {field}"
                    }, HTTPStatus.BAD_REQUEST

            expense = Expense(
                name=expense_data["name"],
                currency=expense_data["currency"],
                price=expense_data["price"],
                payer=expense_data["payer"],
                bill_id=bill_id,
            )

            participants = expense_data.get("participants", [])
            valid_participants = [user.id for user in bill.users] + [
                bill.user_creator_id
            ]

            if not set(participants).issubset(valid_participants):
                return {
                    "message": "Invalid participants specified"
                }, HTTPStatus.BAD_REQUEST

            db.session.add(expense)
            db.session.flush()

            self._create_expense_participants(expense, participants)

            bill.total_sum += expense.price
            db.session.commit()

            logger.info(
                f"Expense created with ID {expense.id} by user {self.current_user}"
            )

            return {"expense": expense.to_dict()}, HTTPStatus.CREATED

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during expense creation: {str(e)}")
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            logger.error(f"Unexpected error during expense creation: {str(e)}")
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def modify_expense(self, expense_id, expense_data):
        try:
            expense = Expense.query.get(expense_id)
            if not expense:
                return {"message": "Expense not found"}, HTTPStatus.NOT_FOUND

            bill = expense.bill
            if not self._is_user_participant(bill):
                return {
                    "message": "User is not a participant of the bill"
                }, HTTPStatus.FORBIDDEN

            participants = expense_data.get("participants", [])
            valid_participants = [user.id for user in bill.users] + [
                bill.user_creator_id
            ]
            if participants and not set(participants).issubset(valid_participants):
                return {
                    "message": "Invalid participants specified"
                }, HTTPStatus.BAD_REQUEST
            self._update_expense_fields(expense, expense_data)

            if "participants" in expense_data:
                self._create_expense_participants(expense, participants)

            db.session.commit()

            logger.info(f"Expense {expense_id} modified by user {self.current_user}")
            return {"expense": expense.to_dict()}, HTTPStatus.OK

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during expense modification: {str(e)}")
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            logger.error(f"Unexpected error during expense modification: {str(e)}")
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def delete_expense(self, expense_id):
        try:
            expense = Expense.query.get(expense_id)
            if not expense:
                return {"message": "Expense not found"}, HTTPStatus.NOT_FOUND

            bill = expense.bill
            if not self._is_user_participant(bill):
                return {
                    "message": "User is not a participant of the bill"
                }, HTTPStatus.FORBIDDEN

            db.session.delete(expense)
            db.session.commit()

            logger.info(f"Expense {expense_id} deleted by user {self.current_user}")
            return {"message": "Expense deleted successfully"}, HTTPStatus.OK
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def _update_expense_fields(self, expense, expense_data):
        updatable_fields = ["name", "currency", "price", "payer", "participants"]
        updatable_fields = ["name", "currency", "price", "payer", "participants"]
        for field in updatable_fields:
            if field in expense_data:
                setattr(expense, field, expense_data[field])

    def _create_expense_participants(self, expense, participants):
        num_participants = len(participants)
        if num_participants > 0:
            amount_per_user = round(expense.price / (num_participants), 2)

            for user in participants:
                expense_participant = ExpenseParticipant(
                    expense_id=expense.id, user_id=user, amount_owed=amount_per_user
                )
                db.session.add(expense_participant)

                debt = Debt(
                    creditor_id=expense.payer,
                    debtor_id=user,
                    amount=amount_per_user,
                    expense_id=expense.id,
                )
                db.session.add(debt)

            db.session.commit()

    def _is_user_participant(self, bill):
        return (
            self.current_user in [user.id for user in bill.users]
            or self.current_user == bill.user_creator_id
        )
