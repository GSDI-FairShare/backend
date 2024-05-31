from pydantic import BaseModel
from typing import Optional
from src.models.request.group_member import GroupMember


class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None


class GroupCreate(GroupBase):
    owner_id: int  # Nuevo campo


class GroupUpdate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    owner_id: int  # Nuevo campo
    members: list[GroupMember] = []

    class Config:
        from_attributes = True
