from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.services.auth_service import AuthService
from src.models.request.user import User, UserCreate
from src.auth.hash_password import HashPassword
from src.models.response.token import TokenResponse
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

hash_password = HashPassword()


@router.post("/signup", response_model=User)
def sign_user_up(user: UserCreate, db: Session = Depends(get_db)):
    auth_service: AuthService = AuthService(db)
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    return auth_service.signup(user)


@router.post("/signin", response_model=TokenResponse)
def sign_user_in(
    user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    auth_service: AuthService = AuthService(db)
    return auth_service.signin(user)
