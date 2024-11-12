from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Bill(db.Model):
    __tablename__ = 'bill'

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_creator_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_added_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    expense_id = db.Column(
        db.Integer, db.ForeignKey("expense.id"), nullable=True)
    name = db.Column(db.String, nullable=False)
    label = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    total_sum = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)

    user_creator = relationship(
        "User", foreign_keys=[user_creator_id], back_populates="bills_created")
    user_added = relationship("User", foreign_keys=[
                              user_added_id], back_populates="bills_added")
    expense = relationship("Expense", back_populates="bills")

    def to_dict(self):
        return {
            "id": self.id,
            "user_creator_id": self.user_creator_id,
            "user_added_id": self.user_added_id,
            "expense_id": self.expense_id,
            "name": self.name,
            "label": self.label,
            "status": self.status,
            "total_sum": self.total_sum,
            "created_at": self.created_at.isoformat()
        }
