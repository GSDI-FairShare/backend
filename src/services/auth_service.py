from sqlalchemy.orm import Session
from src.services.user_service import UserService
from src.models.request.user import UserCreate


class AuthService:
    def __init__(self, db: Session):
        self.user_service: UserService = UserService(db)

    def signup(self, user: UserCreate):
        return self.user_service.create(user)
