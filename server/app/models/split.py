from app import db


class Split(db.Model):
    __tablename__ = "split"

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey("expense.id"), nullable=False)
    split_amount = db.Column(db.Float, nullable=True)

    # expense = db.relationship("exepnse", secondary="split_expense",
    #                           back_populates="split")

    # user = db.relationship("user", secondary="split_user",
    #                           back_populates="split")

    def to_dict(self):
        return {
            "id": self.id,
            "expense_id": self.expense_id,
            "user_id": self.user_id,
            "split_amount": self.split_amount,
        }
