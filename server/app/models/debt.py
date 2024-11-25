from app import db


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creditor_id = db.Column(db.Integer, db.ForeginKey("user.id"))
    debtor_id = db.Column(db.Integer, db.ForeginKey("user.id"))
    amount = db.Column(db.Integer, default=0)
    bill_id = db.Column(db.Integer, db.ForeignKey("bill.id"), nullable=False)
