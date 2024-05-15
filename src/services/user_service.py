from sqlalchemy.orm import Session
from src.repository.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.ticket_repository: UserRepository = UserRepository(db)

    def get_users(self):
        return self.ticket_repository.find_all()

    def create_user(self, user):
        return self.ticket_repository.create(user)
