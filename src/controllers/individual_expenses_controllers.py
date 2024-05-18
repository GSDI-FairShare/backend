from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.auth.authenticate import authenticate
from src.database.connection import get_db
from src.models.request.individual_expenses import (
    IndividualExpenses,
    IndividualExpensesBase,
)
from src.services.individual_expenses_service import (
    IndividualExpensesService,
    create_individual_expenses_service,
)

router = APIRouter()


def get_individual_expenses_service(
    db: Session = Depends(get_db),
) -> IndividualExpensesService:
    return create_individual_expenses_service(db)


@router.post(
    "/expenses", response_model=IndividualExpenses, tags=["Individual Expenses"]
)
def create_expense(
    expense: IndividualExpensesBase,
    user_id: int = Depends(authenticate),
    expenses_service: IndividualExpensesService = Depends(
        get_individual_expenses_service
    ),
):
    return expenses_service.create(user_id, expense)


@router.get(
    "/expenses", response_model=list[IndividualExpenses], tags=["Individual Expenses"]
)
def get_expenses(
    user_id: int = Depends(authenticate),
    expenses_service: IndividualExpensesService = Depends(
        get_individual_expenses_service
    ),
):
    return expenses_service.get_expenses(user_id)


@router.get("/expenses/{expense_id}", tags=["Individual Expenses"])
def get_expense(
    expense_id: int,
    user_id: int = Depends(authenticate),
    expenses_service: IndividualExpensesService = Depends(
        get_individual_expenses_service
    ),
):
    return expenses_service.get_expense(user_id, expense_id)


@router.put("/expenses/{expense_id}", tags=["Individual Expenses"])
def update_expense(
    expense_id: int,
    expense: IndividualExpensesBase,
    user_id: int = Depends(authenticate),
    expenses_service: IndividualExpensesService = Depends(
        get_individual_expenses_service
    ),
):
    return expenses_service.update_expense(user_id, expense_id, expense)


@router.delete("/expenses/{expense_id}", tags=["Individual Expenses"])
def delete_expense(
    expense_id: int,
    user_id: int = Depends(authenticate),
    expenses_service: IndividualExpensesService = Depends(
        get_individual_expenses_service
    ),
):
    return expenses_service.delete_expense(user_id, expense_id)
