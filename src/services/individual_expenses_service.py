from sqlalchemy.orm import Session
from src.models.request.individual_expenses import (
    IndividualExpensesBase,
    IndividualExpensesCreate,
)
from src.repository.individual_expenses_repository import IndividualExpensesRepository
from src.models.data.individual_expenses import IndividualExpenses
from typing import List, Optional
from fastapi import HTTPException, status


class IndividualExpensesService:
    def __init__(self, expenses_repository: IndividualExpensesRepository):
        self.expenses_repository = expenses_repository

    def create(
        self, user_id: int, expense: IndividualExpensesBase
    ) -> IndividualExpensesCreate:
        expense_data = expense.model_dump()
        expense_create = IndividualExpensesCreate(**expense_data, user_id=user_id)
        return self.expenses_repository.save(expense_create)

    def get_expenses(self, user_id: int) -> List[IndividualExpenses]:
        return self.expenses_repository.find_by_user_id(user_id)

    def get_expense(
        self, user_id: int, expense_id: int
    ) -> Optional[IndividualExpensesCreate]:
        expense = self.expenses_repository.find_by_id(user_id, expense_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Expense with id {expense_id} for user {user_id} not found",
            )
        return expense

    def update_expense(
        self, user_id: int, expense_id: int, expense: IndividualExpensesBase
    ) -> Optional[IndividualExpensesCreate]:
        existing_expense = self.get_expense(user_id, expense_id)
        if not existing_expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Expense with id {expense_id} for user {user_id} not found",
            )
        expense_data = expense.model_dump()
        expense_base = IndividualExpensesBase(**expense_data)
        return self.expenses_repository.update_by_id(user_id, expense_id, expense_base)

    def delete_expense(self, user_id: int, expense_id: int) -> None:
        existing_expense = self.get_expense(user_id, expense_id)
        if not existing_expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Expense with id {expense_id} for user {user_id} not found",
            )
        self.expenses_repository.delete_by_id(user_id, expense_id)


# Factory function to create an instance of the service
def create_individual_expenses_service(db: Session) -> IndividualExpensesService:
    expenses_repository = IndividualExpensesRepository(db)
    return IndividualExpensesService(expenses_repository)
