from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.connection import get_db

from src.services.auth_service import AuthService
from src.models.request.user import User, UserCreate

router = APIRouter()


@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    auth_service: AuthService = AuthService(db)
    return auth_service.register(user)
