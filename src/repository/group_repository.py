from typing import List

from sqlalchemy.orm import Session
from src.models.data.group import Group
from src.models.data.group_member import GroupMember
from src.models.data.user import User
from src.models.request.group import GroupCreate


class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, group: GroupCreate) -> Group:
        db_group = Group(**group.model_dump())  # Usar model_dump en lugar de dict
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)
        return db_group

    def find_all(self) -> List[Group]:
        return self.db.query(Group).all()

    def find_by_id(self, group_id: int) -> Group:
        return self.db.query(Group).filter(Group.id == group_id).first()

    def update_by_id(self, group_id: int, group: GroupCreate) -> Group:
        db_group = self.find_by_id(group_id)
        if db_group:
            for (
                key,
                value,
            ) in group.model_dump().items():  # Usar model_dump en lugar de dict
                setattr(db_group, key, value)
            self.db.commit()
            self.db.refresh(db_group)
        return db_group

    def delete_by_id(self, group_id: int) -> None:
        db_group = self.find_by_id(group_id)
        if db_group:
            self.db.delete(db_group)
            self.db.commit()

    def find_by_user_id(self, user_id: int) -> List[Group]:
        return (
            self.db.query(Group)
            .join(Group.members)
            .filter(GroupMember.user_id == user_id)
            .all()
        )

    def find_by_owner_id(self, owner_id: int) -> List[Group]:
        return self.db.query(Group).filter(Group.owner_id == owner_id).all()
