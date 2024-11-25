from app import db


class Expense(db.Model):
    __tablename__ = "expense"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    price = db.Column(db.Float, nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    bill_id = db.Column(db.Integer, db.ForeignKey("bill.id"), nullable=False)

    bill = db.relationship("Bill", back_populates="expenses")
    payer = db.relationship("User", foreign_keys=[payer_id])
    participants = db.relationship(
        "User",
        secondary="expense_participant",
        back_populates="expenses_participated",
        lazy="dynamic",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "currency": self.currency,
            "price": self.price,
            "participants": [user.id for user in self.participants],
        }


class ExpenseParticipant(db.Model):
    __tablename__ = "expense_participant"

    expense_id = db.Column(db.Integer, db.ForeignKey("expense.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    share_amount = db.Column(db.Float, nullable=False)
