from app import db
from app.services.user_service import get_user_by_id


class ExpenseParticipant(db.Model):
    __tablename__ = "expense_participant"
    __mapper_args__ = {"confirm_deleted_rows": False}

    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(
        db.Integer, db.ForeignKey("expense.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount_owed = db.Column(db.Float, nullable=False)

    expense = db.relationship("Expense", back_populates="participants")
    user = db.relationship("User", back_populates="expense_participants")


class Expense(db.Model):
    __tablename__ = "expense"
    __mapper_args__ = {"confirm_deleted_rows": False}

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False)
    currency = db.Column(db.String, nullable=False, default="USD")
    price = db.Column(db.Float, nullable=False)
    payer = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    bill_id = db.Column(
        db.Integer, db.ForeignKey("bill.id", ondelete="CASCADE"), nullable=False
    )

    bill = db.relationship("Bill", back_populates="expenses")
    participants = db.relationship(
        "ExpenseParticipant",
        back_populates="expense",
        cascade="all, delete-orphan",
    )
    debts = db.relationship(
        "Debt",
        cascade="all, delete-orphan",
        back_populates="expense",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "currency": self.currency,
            "price": self.price,
            "payer": get_user_by_id(self.payer).to_dict(),
            "participants": [
                {
                    "user": participant.user.to_dict() if participant.user else None,
                    "amount_owed": participant.amount_owed,
                }
                for participant in self.participants
            ],
        }
