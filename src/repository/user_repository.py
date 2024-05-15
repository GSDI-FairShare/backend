from sqlalchemy.orm import Session

from src.models.data.user import User

from src.models.request.user import UserCreate


class UserRepository:
    def __init__(self, sess: Session):
        self.db: Session = sess

    def find_all(self):
        return self.db.query(User).all()

    def create(self, user: UserCreate):
        hashed_password = user.password
        user = User(email=user.email, username=user.username, password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
