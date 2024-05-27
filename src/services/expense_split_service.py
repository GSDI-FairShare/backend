from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.models.data.expense_split import ExpenseSplit
from src.models.request.expense_split import (
    ExpenseSplitBase,
    ExpenseSplitCreate,
    ExpenseSplitUpdate,
)
from src.repository.expense_split_repository import ExpenseSplitRepository


class ExpenseSplitService:
    def __init__(self, expenses_repository: ExpenseSplitRepository):
        self.expenses_repository = expenses_repository

    def create_split_expense(self, expense: ExpenseSplitCreate) -> ExpenseSplit:
        return self.expenses_repository.save(expense)

    def get_split_expenses(self, user_id: int) -> List[ExpenseSplit]:
        return self.expenses_repository.find_by_user_id(user_id)

    def get_split_expense(
        self, user_id: int, expense_id: int
    ) -> Optional[ExpenseSplit]:
        expense = self.expenses_repository.find_by_id(user_id, expense_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Expense with id {expense_id} for user {user_id} not found",
            )
        return expense

    def update_split_expense(
        self, user_id: int, expense_id: int, expense: ExpenseSplitUpdate
    ) -> Optional[ExpenseSplit]:
        existing_expense = self.get_split_expense(user_id, expense_id)
        if not existing_expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Expense with id {expense_id} for user {user_id} not found",
            )
        expense_data = expense.model_dump()
        expense_base = ExpenseSplitBase(**expense_data)
        return self.expenses_repository.update_by_id(user_id, expense_id, expense_base)

    def delete_split_expense(self, user_id: int, expense_id: int) -> None:
        existing_expense = self.get_split_expense(user_id, expense_id)
        if not existing_expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Expense with id {expense_id} for user {user_id} not found",
            )
        self.expenses_repository.delete_by_id(user_id, expense_id)


def create_expense_split_service(db: Session) -> ExpenseSplitService:
    return ExpenseSplitService(ExpenseSplitRepository(db))
