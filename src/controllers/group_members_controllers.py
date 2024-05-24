from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.models.request.group_member import GroupMemberCreate, GroupMember
from src.services.group_members_service import (
    GroupMembersService,
    create_group_members_service,
)
from src.database.connection import get_db

router = APIRouter()


def get_group_members_service(
    db: Session = Depends(get_db),
) -> GroupMembersService:
    return create_group_members_service(db)


@router.post("/group_members", response_model=GroupMember, tags=["Group Members"])
def add_group_member(
    group_member: GroupMemberCreate,
    service: GroupMembersService = Depends(get_group_members_service),
):
    return service.add_member(group_member.user_id, group_member.group_id)


@router.get("/group_members", response_model=List[GroupMember], tags=["Group Members"])
def list_group_members(
    service: GroupMembersService = Depends(get_group_members_service),
):
    return service.get_group_members()


@router.get(
    "/group_members/{group_member_id}",
    response_model=GroupMember,
    tags=["Group Members"],
)
def get_group_member(
    group_member_id: int,
    service: GroupMembersService = Depends(get_group_members_service),
):
    return service.get_group_member(group_member_id)


@router.put(
    "/group_members/{group_member_id}",
    response_model=GroupMember,
    tags=["Group Members"],
)
def update_group_member(
    group_member_id: int,
    group_member: GroupMember,
    service: GroupMembersService = Depends(get_group_members_service),
):
    return service.update_group_member(group_member_id, group_member)


@router.delete(
    "/group_membermembers/{group_member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Group Members"],
)
def delete_group_member(
    group_member_id: int,
    service: GroupMembersService = Depends(get_group_members_service),
):
    service.delete_group_member(group_member_id)
    return {"message": "Group member deleted successfully"}


@router.get(
    "/users/{user_id}/group_members",
    response_model=List[GroupMember],
    tags=["Group Members"],
)
def get_user_group_members(
    user_id: int,
    service: GroupMembersService = Depends(get_group_members_service),
):
    return service.get_group_members_by_user_id(user_id)


@router.get(
    "/groups/{group_id}/group_members",
    response_model=List[GroupMember],
    tags=["Group Members"],
)
def get_group_group_members(
    group_id: int,
    service: GroupMembersService = Depends(get_group_members_service),
):
    return service.get_group_members_by_group_id(group_id)
