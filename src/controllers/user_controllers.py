from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth.authenticate import authenticate
from src.database.connection import get_db
from src.services.user_service import UserService, create_user_service
from src.models.request.user import User, UserCreate

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return create_user_service(db)


# @router.get("/users", response_model=list[User])
# def get_users(user_service: UserService = Depends(get_user_service)):
#     return user_service.get_users()
#
#
# @router.post("/users", response_model=User)
# def create_user(
#     user: UserCreate, user_service: UserService = Depends(get_user_service)
# ):
#     return user_service.create(user)


@router.get("/users/email/{email}", response_model=User, tags=["Users"])
def get_user_by_email(
    email: str,
    user_id: int = Depends(authenticate),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.find_by_email(email)


@router.get("/users/{user_id}", response_model=User, tags=["Users"])
def get_user_by_id(
    user_id: int,
    user: int = Depends(authenticate),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.find_by_id(user_id)
