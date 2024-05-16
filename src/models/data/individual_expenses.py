from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from src.database.connection import Base


class IndividualExpenses(Base):
    __tablename__ = "individual_expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    description = Column(String)
    amount = Column(Numeric(10, 2))  # Assuming amount is a decimal number

    # Define relationship with User model
    user = relationship("User", back_populates="expenses")
