from sqlalchemy.orm import Session
from src.models.request.group import GroupCreate
from src.repository.group_repository import GroupRepository
from src.models.data.group import Group
from typing import List
from fastapi import HTTPException, status


class GroupService:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    def create(self, user_id: int, group: GroupCreate) -> Group:
        group_data = group.model_dump()
        group_create = GroupCreate(**group_data)
        return self.group_repository.save(user_id, group_create)

    def get_groups(self) -> List[Group]:
        return self.group_repository.find_all()

    def get_group(self, group_id: int) -> Group:
        group = self.group_repository.find_by_id(group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group with id {group_id} not found",
            )
        return group

    def update_group(self, group_id: int, group: GroupCreate) -> Group:
        existing_group = self.get_group(group_id)
        if not existing_group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group with id {group_id} not found",
            )
        group_data = group.model_dump()
        group_base = GroupCreate(**group_data)
        return self.group_repository.update_by_id(group_id, group_base)

    def delete_group(self, group_id: int) -> None:
        existing_group = self.get_group(group_id)
        if not existing_group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group with id {group_id} not found",
            )
        self.group_repository.delete_by_id(group_id)

    def get_my_groups(self, user_id: int) -> List[Group]:
        return self.group_repository.find_by_user_id(user_id)


def create_group_service(db: Session) -> GroupService:
    return GroupService(GroupRepository(db))
