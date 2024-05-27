from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from src.auth.authenticate import authenticate
from src.database.connection import get_db
from src.services.expense_service import ExpenseService, create_expense_service
from src.models.request.expense import (
    ExpenseBase,
    Expense,
)

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