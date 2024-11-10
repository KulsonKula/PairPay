from .imports import *


class group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, index=True)
    user_lider = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_member = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

 # Relacja z liderem (user_lider) w tabeli user
    lider = relationship("user", back_populates="groups_led",
                         foreign_keys=[user_lider])

    # Relacja z członkiem (user_member) w tabeli user
    member = relationship(
        "user", back_populates="groups_member", foreign_keys=[user_member])
