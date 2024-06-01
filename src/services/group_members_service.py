from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.repository.group_members_repository import GroupMembersRepository
from src.services.user_service import UserService, create_user_service
from src.models.data.group_member import GroupMember
from typing import List


class GroupMembersService:
    def __init__(
        self,
        group_members_repository: GroupMembersRepository,
        user_service: UserService,
    ):
        self.group_members_repository = group_members_repository
        self.user_service = user_service

    def add_member(self, user_id: int, group_id: int) -> GroupMember:
        self.user_service.find_by_id(user_id)

        # Verificar si el usuario ya es miembro del grupo
        existing_member = self.group_members_repository.find_by_user_and_group(
            user_id, group_id
        )
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a member of the group",
            )

        return self.group_members_repository.save(user_id, group_id)

    def get_group_members(self) -> List[GroupMember]:
        return self.group_members_repository.find_all()

    def get_group_member(self, group_member_id: int) -> GroupMember:
        group_member = self.group_members_repository.find_by_id(group_member_id)
        if not group_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group member with id {group_member_id} not found",
            )
        return group_member

    def update_group_member(
        self, group_member_id: int, group_member: GroupMember
    ) -> GroupMember:
        existing_group_member = self.get_group_member(group_member_id)
        if not existing_group_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group member with id {group_member_id} not found",
            )
        return self.group_members_repository.update_by_id(group_member_id, group_member)

    def delete_group_member(self, group_member_id: int) -> None:
        existing_group_member = self.get_group_member(group_member_id)
        if not existing_group_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group member with id {group_member_id} not found",
            )
        self.group_members_repository.delete_by_id(group_member_id)

    def get_group_members_by_user_id(self, user_id: int) -> List[GroupMember]:
        return self.group_members_repository.find_by_user_id(user_id)

    def get_group_members_by_group_id(self, group_id: int) -> List[GroupMember]:
        return self.group_members_repository.find_by_group_id(group_id)

    def is_user_member_of_group(self, user_id: int, group_id: int) -> bool:
        return (
            self.group_members_repository.find_by_user_and_group(user_id, group_id)
            is not None
        )


def create_group_members_service(db: Session) -> GroupMembersService:
    group_members_repository = GroupMembersRepository(db)
    user_service = create_user_service(db)
    return GroupMembersService(group_members_repository, user_service)
