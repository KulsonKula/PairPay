from app import db


class Expense(db.Model):
    __tablename__ = "expense"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False)
    currency = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    payer = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    bill_id = db.Column(db.Integer, db.ForeignKey("bill.id"), nullable=False)

    bill = db.relationship("Bill", back_populates="expenses")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "currency": self.currency,
            "price": self.price,
        }
