from app import db
from sqlalchemy.sql import func

bill_user = db.Table(
    "bill_user",
    db.Column("bill_id", db.Integer, db.ForeignKey("bill.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class Bill(db.Model):
    __tablename__ = "bill"

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    label = db.Column(db.String, nullable=True)
    status = db.Column(db.Integer, nullable=False)
    total_sum = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    user_creator = db.relationship(
        "User", foreign_keys=[user_creator_id], back_populates="bills_created"
    )

    users = db.relationship("User", secondary=bill_user, back_populates="bills")

    expenses = db.relationship("Expense", back_populates="bill")

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
            "created_at": self.created_at.isoformat(),
        }
