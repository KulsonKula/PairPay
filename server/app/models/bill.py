from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.db_config import Base


class Bill(Base):
    __tablename__ = 'bill'

    id = Column(Integer, primary_key=True, index=True)
    user_creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_added_id = Column(Integer, ForeignKey("user.id"))
    expense_id = Column(Integer, ForeignKey("expense.id"), nullable=True)
    name = Column(String, nullable=False)
    label = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    total_sum = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user_creator = relationship(
        "User", foreign_keys=[user_creator_id], back_populates="bills_created"
    )
    user_added = relationship(
        "User", foreign_keys=[user_added_id], back_populates="bills_added"
    )
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
            "created_at": self.created_at,
        }
