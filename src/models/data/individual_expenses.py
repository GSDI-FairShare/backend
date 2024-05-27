from sqlalchemy import Column, Float, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from src.database.connection import Base


class IndividualExpenses(Base):
    __tablename__ = "individual_expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    description = Column(String)
    amount = Column(Float, nullable=False)

    # Define relationship with User model
    user = relationship("User", back_populates="individual_expenses")
