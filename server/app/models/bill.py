from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from app.db import Base


class bill(Base):
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
