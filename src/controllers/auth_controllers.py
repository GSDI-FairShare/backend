from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.services.auth_service import AuthService, create_auth_service
from src.models.request.user import User, UserCreate
from src.models.response.token import TokenResponse
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return create_auth_service(db)


@router.post("/signup", response_model=User)
def sign_user_up(
    user: UserCreate, auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.signup(user)


@router.post("/signin", response_model=TokenResponse)
def sign_user_in(
    user: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.signin(user)
