from typing import List

from sqlalchemy.orm import Session
from src.models.data.individual_expenses import IndividualExpenses
from src.models.data.user import User
from src.models.request.individual_expenses import (
    IndividualExpensesCreate,
    IndividualExpensesBase,
)


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

    def find_by_id(self, user_id: int, expense_id: int) -> IndividualExpenses:
        return (
            self.db.query(IndividualExpenses)
            .filter_by(id=expense_id, user_id=user_id)
            .first()
        )

    def update_by_id(
        self, user_id: int, expense_id: int, expense: IndividualExpensesBase
    ) -> IndividualExpenses:
        self.db.query(IndividualExpenses).filter_by(
            id=expense_id, user_id=user_id
        ).update(
            {
                "date": expense.date,
                "description": expense.description,
                "amount": expense.amount,
            }
        )
        self.db.commit()
        return self.find_by_id(user_id, expense_id)

    def delete_by_id(self, user_id: int, expense_id: int) -> None:
        self.db.query(IndividualExpenses).filter_by(
            id=expense_id, user_id=user_id
        ).delete()
        self.db.commit()
