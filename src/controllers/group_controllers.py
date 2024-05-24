from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.auth.authenticate import authenticate
from src.database.connection import get_db
from src.services.group_service import GroupService, create_group_service
from src.models.request.group import GroupCreate, Group

router = APIRouter()


def get_group_service(
    db: Session = Depends(get_db),
) -> GroupService:
    return create_group_service(db)


@router.post("/groups", response_model=Group, tags=["Groups"])
def create_group(
    group: GroupCreate,
    user_id: int = Depends(authenticate),
    group_service: GroupService = Depends(get_group_service),
):
    return group_service.create(user_id, group)


@router.get("/groups", response_model=list[Group], tags=["Groups"])
def get_groups(
    user_id: int = Depends(authenticate),
    group_service: GroupService = Depends(get_group_service),
):
    return group_service.get_groups()


@router.get("/me/groups", response_model=list[Group], tags=["Groups"])
def get_my_groups(
    user_id: int = Depends(authenticate),
    group_service: GroupService = Depends(get_group_service),
):
    return group_service.get_my_groups(user_id)
