from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.repository.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.user_repository: UserRepository = UserRepository(db)

    def get_users(self):
        return self.user_repository.find_all()

    def create(self, user):
        bd_user = self.user_repository.find_by_email(email=user.email)
        if bd_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return self.user_repository.save(user)

    def find_by_email(self, email):
        db_user = self.user_repository.find_by_email(email=email)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
