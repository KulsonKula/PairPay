from logging import Logger
from app import db
from app.models import Expense, Bill, User
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus

logger = Logger(__name__)


class ExpenseService:
    def __init__(self, current_user):
        self.current_user = current_user

    def get_expenses(self, bill_id):
        try:
            bill = Bill.query.get(bill_id)
            if not bill:
                return {"message": "Bill not found"}, HTTPStatus.NOT_FOUND

            if (
                self.current_user not in [user.id for user in bill.users]
                and self.current_user != bill.user_creator_id
            ):
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

            if (
                self.current_user not in [user.id for user in bill.users]
                and self.current_user != bill.user_creator_id
            ):
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

            logger.info(
                f"Current user: {self.current_user}, Bill creator: {bill.user_creator_id}, "
                f"Participants: {[user.id for user in bill.users]}"
            )

            if (
                self.current_user not in [user.id for user in bill.users]
                and self.current_user != bill.user_creator_id
            ):
                return {
                    "message": "User is not a participant of the bill"
                }, HTTPStatus.FORBIDDEN

            expense = Expense(
                name=expense_data.get("name"),
                currency=expense_data.get("currency"),
                price=expense_data.get("price"),
                payer=expense_data.get("payer"),
                bill_id=bill_id,
            )

            users = expense_data.get("users", [])
            if users:
                valid_users = [user.id for user in bill.users] + [bill.user_creator_id]
                valid_users = User.query.filter(User.id.in_(valid_users)).all()
                for user in valid_users:
                    if user.id in users:
                        expense.users.append(user)

            db.session.add(expense)
            db.session.commit()

            logger.info(
                f"Expense created with ID {expense.id} by user {self.current_user}"
            )

            return {"expense": expense.to_dict()}, HTTPStatus.CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def modify_expense(self, expense_id, expense_data):
        try:
            expense = Expense.query.get(expense_id)
            if not expense:
                return {"message": "Expense not found"}, HTTPStatus.NOT_FOUND

            bill = expense.bill
            if (
                self.current_user not in [user.id for user in bill.users]
                and self.current_user != bill.user_creator_id
            ):
                return {
                    "message": "User is not a participant of the bill"
                }, HTTPStatus.FORBIDDEN

            users = expense_data.get("users", [])
            if users:
                valid_users = [user.id for user in bill.users] + [bill.user_creator_id]
                valid_users = User.query.filter(User.id.in_(valid_users)).all()

                expense.users = [
                    user for user in expense.users if user.id in valid_users
                ]
                for user in valid_users:
                    if user.id in users and user not in expense.users:
                        expense.users.append(user)

            self._update_expense_fields(expense, expense_data)
            db.session.commit()

            logger.info(f"Expense {expense_id} modified by user {self.current_user}")

            return {"expense": expense.to_dict()}, HTTPStatus.OK
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def delete_expense(self, expense_id):
        try:
            expense = Expense.query.get(expense_id)
            if not expense:
                return {"message": "Expense not found"}, HTTPStatus.NOT_FOUND

            bill = expense.bill
            if (
                self.current_user not in [user.id for user in bill.users]
                and self.current_user != bill.user_creator_id
            ):
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
        updatable_fields = ["name", "currency", "price", "payer", "users"]
        for field in updatable_fields:
            if field in expense_data:
                setattr(expense, field, expense_data[field])
