from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    password = Column(String)

    # Add relationship with IndividualExpenses model
    expenses = relationship("IndividualExpenses", back_populates="user")
