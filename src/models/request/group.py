from pydantic import BaseModel
from typing import Optional


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

    class Config:
        from_attributes = True
