from sqlalchemy.orm import Session

from src.models.data.user import User


class UserRepository:
    def __init__(self, sess: Session):
        self.db: Session = sess

    def find_all(self):
        return self.db.query(User).all()
