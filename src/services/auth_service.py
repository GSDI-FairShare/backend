from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.services.user_service import UserService
from src.models.request.user import UserCreate
from src.auth.hash_password import HashPassword
from src.auth.jwt_handler import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

hash_password = HashPassword()


class AuthService:
    def __init__(self, db: Session):
        self.user_service: UserService = UserService(db)

    def signup(self, user: UserCreate):
        return self.user_service.create(user)

    def signin(self, user: OAuth2PasswordRequestForm):
        user_db = self.user_service.find_by_email(user.username)
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        if not hash_password.verify_hash(user.password, user_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        access_token = create_access_token(user_db.id)
        return {"access_token": access_token, "token_type": "Bearer"}
