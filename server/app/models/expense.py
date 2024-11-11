from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.db_config import Base


class Expense(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    currency = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    bills = relationship("Bill", back_populates="expense")
