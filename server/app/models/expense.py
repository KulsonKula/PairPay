from .imports import *


class expense(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    currency = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
