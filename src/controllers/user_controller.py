from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.services.user_service import UserService
from src.models.request.user import User, UserCreate

router = APIRouter()


@router.get("/users", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    user_service: UserService = UserService(db)
    return user_service.get_users()


@router.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service: UserService = UserService(db)
    return user_service.create_user(user)
