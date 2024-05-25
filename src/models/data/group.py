from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.connection import Base


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Nueva columna

    owner = relationship("User", back_populates="owned_groups")  # Relación con User
    members = relationship("GroupMember", back_populates="group")
    expenses = relationship("Expense", back_populates="group")
