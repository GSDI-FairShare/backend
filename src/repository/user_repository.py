from sqlalchemy.orm import Session

from src.models.data.user import User

from src.models.data.individual_expenses import IndividualExpenses

from src.models.request.user import UserCreate


class UserRepository:
    def __init__(self, sess: Session):
        self.db: Session = sess

    def find_all(self):
        return self.db.query(User).all()

    def save(self, user: UserCreate):
        hashed_password = user.password
        user = User(email=user.email, username=user.username, password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
