from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database.connection import Base


class GroupMember(Base):
    __tablename__ = "group_members"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="groups")
