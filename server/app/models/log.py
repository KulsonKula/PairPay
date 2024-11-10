from .imports import *


class log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    data = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("user", back_populates="log")
