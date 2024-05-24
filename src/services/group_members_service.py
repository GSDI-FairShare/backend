from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.repository.group_members_repository import GroupMembersRepository
from src.repository.user_repository import UserRepository
from src.repository.group_repository import GroupRepository
from src.models.data.group_member import GroupMember
from typing import List


class GroupMembersService:
    def __init__(
        self,
        group_members_repository: GroupMembersRepository,
        user_repository: UserRepository,
        group_repository: GroupRepository,
    ):
        self.group_members_repository = group_members_repository
        self.user_repository = user_repository
        self.group_repository = group_repository

    def add_member(self, user_id: int, group_id: int) -> GroupMember:
        # Verificar si el usuario y el grupo existen
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        group = self.group_repository.find_by_id(group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group with id {group_id} not found",
            )

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


def create_group_members_service(db: Session) -> GroupMembersService:
    group_members_repository = GroupMembersRepository(db)
    user_repository = UserRepository(db)
    group_repository = GroupRepository(db)
    return GroupMembersService(
        group_members_repository, user_repository, group_repository
    )
