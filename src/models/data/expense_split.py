from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from src.database.connection import Base


class ExpenseSplit(Base):
    __tablename__ = "expense_splits"
    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    paid = Column(Boolean, default=False)

    expense = relationship("Expense", back_populates="splits")
    user = relationship("User", back_populates="splits")
