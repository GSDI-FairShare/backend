from sqlalchemy.orm import Session
from src.models.data.user import User
from src.models.data.individual_expenses import IndividualExpenses
from src.models.request.user import UserCreate
from src.auth.hash_password import HashPassword

hash_password = HashPassword()


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(User).all()

    def save(self, user: UserCreate):
        hashed_password = hash_password.create_hash(user.password)
        new_user = User(
            email=user.email, username=user.username, password=hashed_password
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def find_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
