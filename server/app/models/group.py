from .imports import *


class group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, index=True)
    user_lider = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_member = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
