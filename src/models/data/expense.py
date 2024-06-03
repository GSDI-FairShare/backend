from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from src.database.connection import Base
from src.models.data.category import ExpenseCategory
from src.models.data.currency import CurrencyType


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    category = Column(Enum(ExpenseCategory), nullable=True)
    currency = Column(Enum(CurrencyType), nullable=False)
    date = Column(Date, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    group = relationship("Group", back_populates="expenses")
    creator = relationship("User", back_populates="expenses")
    splits = relationship("ExpenseSplit", back_populates="expense")
