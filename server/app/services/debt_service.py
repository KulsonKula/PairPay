from http import HTTPStatus
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models import Expense, ExpenseParticipant


class DebtService:
    def __init__(self, current_user):
        self.current_user = current_user

    def get_user_balances(self):
        try:
            money_owed_to_user = (
                db.session.query(func.sum(ExpenseParticipant.amount_owed))
                .join(Expense)
                .filter(
                    Expense.payer == self.current_user,
                    ExpenseParticipant.user_id != self.current_user,
                )
                .scalar()
                or 0
            )

            money_user_owes = (
                db.session.query(func.sum(ExpenseParticipant.amount_owed))
                .join(Expense)
                .filter(
                    ExpenseParticipant.user_id == self.current_user,
                    Expense.payer != self.current_user,
                )
                .scalar()
                or 0
            )

            net_balance = money_owed_to_user - money_user_owes

            return {"balance": net_balance}, HTTPStatus.OK

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_debt_with_friend(self, friend_id):
        try:
            owed_to_user = (
                db.session.query(func.sum(ExpenseParticipant.amount_owed))
                .join(Expense, ExpenseParticipant.expense_id == Expense.id)
                .filter(Expense.payer == self.current_user)
                .filter(ExpenseParticipant.user_id == friend_id)
                .scalar()
                or 0
            )

            owed_to_friend = (
                db.session.query(func.sum(ExpenseParticipant.amount_owed))
                .join(Expense, ExpenseParticipant.expense_id == Expense.id)
                .filter(Expense.payer == friend_id)
                .filter(ExpenseParticipant.user_id == self.current_user)
                .scalar()
                or 0
            )

            net_debt = owed_to_user - owed_to_friend

            return {
                "net_debt": net_debt,
                "owed_to_user": owed_to_user,
                "owed_to_friend": owed_to_friend,
            }, HTTPStatus.OK

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": f"Database error: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {
                "message": f"An unexpected error occurred: {str(e)}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
