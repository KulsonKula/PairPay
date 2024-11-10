from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db import Base


class log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    data = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
