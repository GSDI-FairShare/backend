from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.auth.authenticate import authenticate
from src.database.connection import get_db
from src.services.group_service import GroupService, create_group_service
from src.models.request.group import GroupBase, Group, GroupUpdate

router = APIRouter()


def get_group_service(
    db: Session = Depends(get_db),
) -> GroupService:
    return create_group_service(db)


@router.post("/groups", response_model=Group, tags=["Groups"])
def create_my_group(
    group: GroupBase,
    user_id: int = Depends(authenticate),
    group_service: GroupService = Depends(get_group_service),
):
    return group_service.create(user_id, group)


@router.get("/groups", response_model=list[Group], tags=["Groups"])
def get_my_groups(
    user_id: int = Depends(authenticate),
    group_service: GroupService = Depends(get_group_service),
):
    return group_service.get_my_groups(user_id)


@router.put("/groups/{group_id}", response_model=Group, tags=["Groups"])
def update_group(
    group_id: int,
    group: GroupUpdate,
    user_id: int = Depends(authenticate),
    group_service: GroupService = Depends(get_group_service),
):
    existing_group = group_service.get_group(group_id)
    if existing_group.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this group",
        )
    return group_service.update_group(group_id, group)


@router.delete(
    "/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Groups"]
)
def delete_group(
    group_id: int,
    user_id: int = Depends(authenticate),
    group_service: GroupService = Depends(get_group_service),
):
    existing_group = group_service.get_group(group_id)
    if existing_group.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this group",
        )
    group_service.delete_group(group_id)
    return {"message": "Group deleted successfully"}
