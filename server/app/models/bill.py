from .imports import *


class bill(Base):
    __tablename__ = 'bill'

    id = Column(Integer, primary_key=True, index=True)
    user_creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_added_id = Column(Integer, ForeignKey("user.id"))
    expense_id = Column(Integer, ForeignKey("expense.id"))
    name = Column(String, nullable=False)
    label = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    total_sum = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user_creator = relationship(
        "user", foreign_keys=[user_creator_id], back_populates="bills_created")
    user_added = relationship("user", foreign_keys=[
                              user_added_id], back_populates="bills_added")
    expense = relationship("expense", back_populates="bills")
