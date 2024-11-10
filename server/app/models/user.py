from .imports import *


class user(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    mail = Column(EmailType, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    admin = Column(Boolean, default=0)
    created_at = Column(DateTime, server_default=func.now())

    bills_created = relationship(
        "bill", foreign_keys="[bill.user_creator_id]", back_populates="user_creator")
    bills_added = relationship(
        "bill", foreign_keys="[bill.user_added_id]", back_populates="user_added")

    # Relacja z group jako lider
    groups_led = relationship(
        "group", back_populates="lider", foreign_keys="[group.user_lider]")

    # Relacja z group jako członek
    groups_member = relationship(
        "group", back_populates="member", foreign_keys="[group.user_member]")

    log = relationship("log", back_populates="user")
