from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.services.user_service import UserService, create_user_service
from src.models.request.user import User, UserCreate

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return create_user_service(db)


@router.get("/users", response_model=list[User])
def get_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_users()


@router.post("/users", response_model=User)
def create_user(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    return user_service.create(user)

@router.get("/users/email/{email}", response_model=User)
def get_user_by_email(
    email: str, user_service: UserService = Depends(get_user_service)
):
    return user_service.find_by_email(email)
