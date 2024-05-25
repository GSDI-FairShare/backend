from typing import List

from sqlalchemy.orm import Session
from src.models.data.group import Group
from src.models.request.group import GroupCreate
from src.models.data.group_member import GroupMember
from src.models.request.group_member import GroupMemberUpdate


class GroupMembersRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[GroupMember]:
        return self.db.query(GroupMember).all()

    def save(self, user_id: int, group_id: int) -> GroupMember:
        new_group_member = GroupMember(user_id=user_id, group_id=group_id)
        self.db.add(new_group_member)
        self.db.commit()
        self.db.refresh(new_group_member)
        return new_group_member

    def find_by_id(self, group_member_id: int) -> GroupMember:
        return self.db.query(GroupMember).filter_by(id=group_member_id).first()

    def update_by_id(
        self, group_member_id: int, group_member: GroupMemberUpdate
    ) -> GroupMember:
        self.db.query(GroupMember).filter_by(id=group_member_id).update(
            {"user_id": group_member.user_id}
        )
        self.db.commit()
        return self.find_by_id(group_member_id)

    def delete_by_id(self, group_member_id: int) -> None:
        self.db.query(GroupMember).filter_by(id=group_member_id).delete()
        self.db.commit()

    def find_by_user_id(self, user_id: int) -> List[GroupMember]:
        return self.db.query(GroupMember).filter_by(user_id=user_id).all()

    def find_by_group_id(self, group_id: int) -> List[GroupMember]:
        return self.db.query(GroupMember).filter_by(group_id=group_id).all()

    def find_by_user_and_group(self, user_id: int, group_id: int) -> GroupMember:
        return (
            self.db.query(GroupMember)
            .filter(GroupMember.user_id == user_id)
            .filter(GroupMember.group_id == group_id)
            .first()
        )
