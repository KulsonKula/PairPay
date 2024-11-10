from .imports import *


class group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, index=True)
    user_lider = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_member = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    leader = relationship("user", foreign_keys=[
                          user_lider], back_populates="groups_led")
    members = relationship("user", foreign_keys=[
                           user_member], back_populates="groups_member")
