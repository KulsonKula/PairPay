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

    log = relationship("log", back_populates="user")
