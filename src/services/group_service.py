from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.models.data.group import Group
from src.models.request.group import GroupCreate
from src.repository.group_repository import GroupRepository
from src.services.group_members_service import (
    GroupMembersService,
    create_group_members_service,
)


class GroupService:
    def __init__(
        self,
        group_repository: GroupRepository,
        group_members_service: GroupMembersService,
    ):
        self.group_repository = group_repository
        self.group_members_service = group_members_service

    def create(self, user_id: int, group: GroupCreate) -> Group:
        group_data = group.model_dump()
        group_create = GroupCreate(**group_data)
        new_group = self.group_repository.save(group_create)
        self.group_members_service.add_member(user_id, new_group.id)
        return new_group

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
    group_repository = GroupRepository(db)
    group_members_service = create_group_members_service(db)
    return GroupService(group_repository, group_members_service)
