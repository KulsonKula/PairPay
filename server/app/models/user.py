from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType
from app.db.db_config import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    mail = Column(EmailType, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    admin = Column(Boolean, default=0)
    created_at = Column(DateTime, server_default=func.now())

    bills_created = relationship(
        "Bill", foreign_keys="[Bill.user_creator_id]", back_populates="user_creator"
    )
    bills_added = relationship(
        "Bill", foreign_keys="[Bill.user_added_id]", back_populates="user_added"
    )

    # Relacja z group jako lider
    groups_led = relationship(
        "Group", back_populates="lider", foreign_keys="[Group.user_lider]"
    )

    # Relacja z group jako członek
    groups_member = relationship(
        "Group", back_populates="member", foreign_keys="[Group.user_member]"
    )

    log = relationship("Log", back_populates="user")
