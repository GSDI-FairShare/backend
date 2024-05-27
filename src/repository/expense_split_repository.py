from typing import List

from sqlalchemy.orm import Session
from src.models.data.expense import Expense
from src.models.data.expense_split import ExpenseSplit
from src.models.data.user import User
from src.models.request.expense_split import (
    ExpenseSplitBase,
    ExpenseSplitCreate,
    ExpenseSplitUpdate,
)


class ExpenseSplitRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def save(self, expense_split: ExpenseSplitCreate) -> ExpenseSplit:
        expense_split = ExpenseSplit(
            expense_id=expense_split.expense_id,
            user_id=expense_split.user_id,
            amount=expense_split.amount,
            percentage=expense_split.percentage,
            paid=expense_split.paid,
        )
        self.db.add(expense_split)
        self.db.commit()
        self.db.refresh(expense_split)
        return expense_split

    def find_by_expense_id(self, expense_id: int) -> List[ExpenseSplit]:
        return self.db.query(ExpenseSplit).filter_by(expense_id=expense_id).all()

    def find_by_id(self, expense_id: int, split_id: int) -> ExpenseSplit:
        return (
            self.db.query(ExpenseSplit)
            .filter_by(id=split_id, expense_id=expense_id)
            .first()
        )

    def update_by_id(
        self, expense_id: int, split_id: int, expense_split: ExpenseSplitBase
    ) -> ExpenseSplit:
        self.db.query(ExpenseSplit).filter_by(
            id=split_id, expense_id=expense_id
        ).update(
            {
                "percentage": expense_split.percentage,
                "paid": expense_split.paid,
            }
        )
        self.db.commit()
        return self.find_by_id(expense_id, split_id)

    def delete_by_id(self, expense_id: int, split_id: int) -> None:
        self.db.query(ExpenseSplit).filter_by(
            id=split_id, expense_id=expense_id
        ).delete()
        self.db.commit()

    def find_by_user_id(self, user_id: int) -> List[ExpenseSplit]:
        return self.db.query(ExpenseSplit).filter_by(user_id=user_id).all()
