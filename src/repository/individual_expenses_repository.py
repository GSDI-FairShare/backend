from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from src.models.data.individual_expenses import IndividualExpenses
from src.models.request.individual_expenses import IndividualExpensesCreate
from src.models.data.user import User


class IndividualExpensesRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def save(self, expense: IndividualExpensesCreate) -> IndividualExpenses:
        try:
            expense = IndividualExpenses(
                user_id=expense.user_id,
                amount=expense.amount,
                description=expense.description,
                date=expense.date,
            )
            self.db.add(expense)
            self.db.commit()
            self.db.refresh(expense)
            return expense
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Error saving expense: {e}")

    def find_by_user_id(self, user_id: int) -> List[IndividualExpenses]:
        try:
            return self.db.query(IndividualExpenses).filter_by(user_id=user_id).all()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error fetching expenses for user {user_id}: {e}")
