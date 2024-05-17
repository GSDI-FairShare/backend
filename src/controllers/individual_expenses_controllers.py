from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.auth.authenticate import authenticate
from src.services.individual_expenses_service import (
    IndividualExpensesService,
    create_individual_expenses_service,
)
from src.models.request.individual_expenses import (
    IndividualExpensesBase,
    IndividualExpenses,
)

router = APIRouter()


def get_individual_expenses_service(
    db: Session = Depends(get_db),
) -> IndividualExpensesService:
    return create_individual_expenses_service(db)


@router.post("/expenses", response_model=IndividualExpenses)
def create_expense(
    expense: IndividualExpensesBase,
    user_id: int = Depends(authenticate),
    expenses_service: IndividualExpensesService = Depends(
        get_individual_expenses_service
    ),
):
    return expenses_service.create(user_id, expense)


@router.get("/expenses", response_model=list[IndividualExpenses])
def get_user_expenses(
    user_id: int = Depends(authenticate),
    expenses_service: IndividualExpensesService = Depends(
        get_individual_expenses_service
    ),
):
    return expenses_service.get_expenses(user_id)
