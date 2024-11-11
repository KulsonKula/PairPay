from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType
from app.db.db_config import Base


class Bill(Base):
    __tablename__ = 'bill'

    id = Column(Integer, primary_key=True, index=True)
    user_creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_added_id = Column(Integer, ForeignKey("user.id"))
    expense_id = Column(Integer, ForeignKey("expense.id"))
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
