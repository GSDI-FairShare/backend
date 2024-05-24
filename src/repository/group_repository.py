from typing import List

from sqlalchemy.orm import Session
from src.models.data.group import Group
from src.models.request.group import GroupCreate
from src.models.data.group_member import GroupMember


class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[Group]:
        return self.db.query(Group).all()

    def save(self, user_id, group: GroupCreate) -> Group:
        new_group = Group(name=group.name, description=group.description)
        new_group_member = GroupMember(user_id=user_id, group=new_group)
        self.db.add(new_group_member)
        self.db.commit()
        self.db.refresh(new_group_member)

        self.db.add(new_group)
        self.db.commit()
        self.db.refresh(new_group)
        return new_group

    def find_by_id(self, group_id: int) -> Group:
        return self.db.query(Group).filter_by(id=group_id).first()

    def update_by_id(self, group_id: int, group: GroupCreate) -> Group:
        self.db.query(Group).filter_by(id=group_id).update({"name": group.name})
        self.db.commit()
        return self.find_by_id(group_id)

    def delete_by_id(self, group_id: int) -> None:
        self.db.query(Group).filter_by(id=group_id).delete()
        self.db.commit()

    def find_by_user_id(self, user_id: int) -> List[Group]:
        return (
            self.db.query(Group)
            .join(GroupMember)
            .filter(GroupMember.user_id == user_id)
            .all()
        )
