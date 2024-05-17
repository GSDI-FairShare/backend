from sqlalchemy.orm import Session
from src.models.data.user import User
from src.models.data.individual_expenses import IndividualExpenses
from src.models.request.user import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(User).all()

    def save(self, user: UserCreate):
        hashed_password = (
            user.password
        )  # Aquí podrías aplicar hash al password si es necesario
        new_user = User(
            email=user.email, username=user.username, password=hashed_password
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def find_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
