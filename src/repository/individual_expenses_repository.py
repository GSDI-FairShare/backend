from sqlalchemy.orm import Session
from src.models.data.user import User
from src.models.data.individual_expenses import IndividualExpenses
from src.models.request.individual_expenses import IndividualExpensesCreate
from typing import List


class IndividualExpensesRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def save(self, expense: IndividualExpensesCreate) -> IndividualExpenses:
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

    def find_by_user_id(self, user_id: int) -> List[IndividualExpenses]:
        return self.db.query(IndividualExpenses).filter_by(user_id=user_id).all()
