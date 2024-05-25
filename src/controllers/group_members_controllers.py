from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.auth.authenticate import authenticate
from src.controllers.group_controllers import get_group_service
from src.database.connection import get_db
from src.models.request.group_member import GroupMember, GroupMemberCreate
from src.services.group_members_service import (
    GroupMembersService,
    create_group_members_service,
)
from src.services.group_service import GroupService

router = APIRouter()


def get_group_members_service(
    db: Session = Depends(get_db),
) -> GroupMembersService:
    return create_group_members_service(db)


@router.post("/group_members", response_model=GroupMember, tags=["Group Members"])
def add_member_to_group(
    group_member_data: GroupMemberCreate,
    user_id: int = Depends(authenticate),
    group_members_service: GroupMembersService = Depends(get_group_members_service),
    group_service: GroupService = Depends(get_group_service),
):
    group = group_service.get_group(group_member_data.group_id)
    if group.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add members to this group",
        )
    return group_members_service.add_member(
        group_member_data.user_id, group_member_data.group_id
    )


@router.get(
    "/my_group_members", response_model=List[GroupMember], tags=["Group Members"]
)
def get_groups_i_am_member_of(
    user_id: int = Depends(authenticate),
    group_members_service: GroupMembersService = Depends(get_group_members_service),
):
    return group_members_service.get_group_members_by_user_id(user_id)


@router.get(
    "/groups/{group_id}/members",
    response_model=List[GroupMember],
    tags=["Group Members"],
)
def get_group_members(
    group_id: int,
    user_id: int = Depends(authenticate),
    group_members_service: GroupMembersService = Depends(get_group_members_service),
):
    return group_members_service.get_group_members_by_group_id(group_id)
