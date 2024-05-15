from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.services.user_service import UserService

router = APIRouter()


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    user_service: UserService = UserService(db)
    return user_service.get_users()
