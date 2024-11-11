from .imports import *
from app.db import Base


class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, index=True)
    user_lider = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_member = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    lider = relationship("User", back_populates="groups_led",
                         foreign_keys=[user_lider])
    member = relationship(
        "User", back_populates="groups_member", foreign_keys=[user_member])
