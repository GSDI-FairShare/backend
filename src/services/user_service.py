from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.repository.user_repository import UserRepository
from src.models.request.user import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.user_repository: UserRepository = UserRepository(db)

    def get_users(self):
        return self.user_repository.find_all()

    def create(self, user: UserCreate):
        bd_user = self.user_repository.find_by_email(user.email)
        if bd_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )
        return self.user_repository.save(user)

    def find_by_email(self, email: str):
        db_user = self.user_repository.find_by_email(email)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return db_user
