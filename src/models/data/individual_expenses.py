from sqlalchemy import Column, Float, Integer, String, Date, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from src.database.connection import Base
from src.models.data.category import ExpenseCategory
from src.models.data.currency import CurrencyType


class IndividualExpenses(Base):
    __tablename__ = "individual_expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    description = Column(String)
    amount = Column(Float, nullable=False)
    category = Column(Enum(ExpenseCategory), nullable=True)
    currency = Column(Enum(CurrencyType), nullable=False)
    paid = Column(Boolean, default=False)

    # Define relationship with User model
    user = relationship("User", back_populates="individual_expenses")
