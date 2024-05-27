from typing import List

from sqlalchemy.orm import Session
from src.models.data.expense import Expense
from src.models.data.expense_split import ExpenseSplit
from src.models.data.user import User
from src.models.data.group import Group

from src.models.request.expense import ExpenseCreate, ExpenseUpdate


class ExpenseRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def save(self, expense: ExpenseCreate) -> Expense:
        expense = Expense(
            group_id=expense.group_id,
            created_by=expense.created_by,
            amount=expense.amount,
            description=expense.description,
            date=expense.date,
        )
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def find_by_id(self, expense_id: int) -> Expense:
        return self.db.query(Expense).filter_by(id=expense_id).first()

    def find_by_group_id(self, group_id: int) -> List[Expense]:
        return self.db.query(Expense).filter_by(group_id=group_id).all()

    def find_by_user_id(self, user_id: int) -> List[Expense]:
        return self.db.query(Expense).filter_by(user_id=user_id).all()

    def update_by_id(self, expense_id: int, expense: ExpenseUpdate) -> Expense:
        self.db.query(Expense).filter_by(id=expense_id).update(
            {
                "amount": expense.amount,
                "description": expense.description,
                "date": expense.date,
            }
        )
        self.db.commit()
        return self.find_by_id(expense_id)

    def delete_by_id(self, expense_id: int) -> None:
        self.db.query(Expense).filter_by(id=expense_id).delete()
        self.db.commit()
