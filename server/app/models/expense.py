from app import db

expense_user = db.Table(
    "expense_user",
    db.Column("expense_id", db.Integer, db.ForeignKey("expense.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class Expense(db.Model):
    __tablename__ = "expense"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False)
    currency = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    payer = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    bill_id = db.Column(db.Integer, db.ForeignKey("bill.id"), nullable=False)

    bill = db.relationship("Bill", back_populates="expenses")
    users = db.relationship("User", secondary="expense_user", back_populates="expenses")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "currency": self.currency,
            "price": self.price,
            "users": [user.id for user in self.users],
        }
