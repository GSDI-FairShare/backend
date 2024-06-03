from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from src.auth.authenticate import authenticate
from src.database.connection import get_db
from src.services.expense_service import ExpenseService, create_expense_service
from src.models.request.expense import (
    ExpenseBase,
    Expense,
)
from src.models.data.category import ExpenseCategory
from src.models.data.currency import CurrencyType

router = APIRouter()


def get_expense_service(db: Session = Depends(get_db)) -> ExpenseService:
    return create_expense_service(db)


@router.post(
    "/groups/{group_id}/expenses", response_model=Expense, tags=["Group Expenses"]
)
def create_expense(
    group_id: int,
    expense: ExpenseBase,
    user_id: int = Depends(authenticate),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.create_expense(user_id, group_id, expense)


@router.get(
    "/groups/{group_id}/expenses", response_model=List[Expense], tags=["Group Expenses"]
)
def get_expenses(
    group_id: int,
    user_id: int = Depends(authenticate),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_expenses(user_id, group_id)


@router.get("/categories", response_model=List[str], tags=["Group Expenses"])
def get_expense_categories():
    return [category.value for category in ExpenseCategory]


@router.get("/currencies", response_model=List[str], tags=["Group Expenses"])
def get_currencies():
    return [currency.value for currency in CurrencyType]
