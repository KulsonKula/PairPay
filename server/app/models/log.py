from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.db_config import Base


class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    data = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="log")
