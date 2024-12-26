from app import db


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creditor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    debtor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount = db.Column(db.Float, default=0)
    expense_id = db.Column(db.Integer, db.ForeignKey("expense.id"), nullable=False)

    creditor = db.relationship("User", foreign_keys=[creditor_id])
    debtor = db.relationship("User", foreign_keys=[debtor_id])
    expense = db.relationship("Expense")
