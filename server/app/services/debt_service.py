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
            paid_by_user = (
                db.session.query(
                    ExpenseParticipant.user_id,
                    func.sum(ExpenseParticipant.amount_owed).label("total_owed"),
                )
                .join(Expense)
                .filter(Expense.payer == self.current_user)
                .group_by(ExpenseParticipant.user_id)
                .all()
            )

            owed_by_user = (
                db.session.query(
                    Expense.payer,
                    func.sum(ExpenseParticipant.amount_owed).label("total_owed"),
                )
                .join(ExpenseParticipant)
                .filter(ExpenseParticipant.user_id == self.current_user)
                .group_by(Expense.payer)
                .all()
            )

            balances = {}

            for user_id, total_owed in paid_by_user:
                balances[user_id] = balances.get(user_id, 0) + total_owed

            for payer_id, total_owed in owed_by_user:
                balances[payer_id] = balances.get(payer_id, 0) - total_owed

            result = [
                {"user_id": user_id, "balance": balance}
                for user_id, balance in balances.items()
                if balance != 0
            ]

            return {"balances": result}, HTTPStatus.OK

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
