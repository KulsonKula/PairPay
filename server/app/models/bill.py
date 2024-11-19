from app import db
from sqlalchemy.sql import func

bill_user = db.Table(
    'bill_user',
    db.Column('bill_id', db.Integer, db.ForeignKey(
        'bill.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id'), primary_key=True)
)

bill_expense = db.Table(
    'bill_expense',
    db.Column('bill_id', db.Integer, db.ForeignKey(
        'bill.id'), primary_key=True),
    db.Column('expense_id', db.Integer, db.ForeignKey(
        'expense.id'), primary_key=True)
)


class Bill(db.Model):
    __tablename__ = 'bill'

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_creator_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    name = db.Column(db.String, nullable=False)
    label = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    total_sum = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)

    user_creator = db.relationship(
        "User", foreign_keys=[user_creator_id], back_populates="bills_created")

    users = db.relationship("User", secondary=bill_user,
                            back_populates="bills")

    expenses = db.relationship(
        "Expense", secondary=bill_expense, back_populates="bills")

    def to_dict(self):
        return {
            "id": self.id,
            "user_creator_id": self.user_creator_id,
            "users": [user.id for user in self.users],
            "expenses": [expense.id for expense in self.expenses],
            "name": self.name,
            "label": self.label,
            "status": self.status,
            "total_sum": self.total_sum,
            "created_at": self.created_at.isoformat()
        }

# MAYBE CHANGE TO STH LIKE THIS

# class BillMembers(db.Model):
#     __tablename__ = 'bill_members'

#     id = db.Column(db.Integer, primary_key=True)
#     bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     bill = db.relationship('Bill', back_populates='users')
#     user = db.relationship('User')

# class BillExpenses(db.Model):
#     __tablename__ = 'bill_expenses'

#     id = db.Column(db.Integer, primary_key=True)
#     bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'))
#     expense_id = db.Column(db.Integer, db.ForeignKey('expense_id'))

#     bill = db.relationship('Bill', backpopulates='expenses')
#     expense = db.relationship('Expense', backpopulates='expenses')
