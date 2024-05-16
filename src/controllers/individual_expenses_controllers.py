from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.auth.authenticate import authenticate
from src.services.individual_expenses_service import IndividualExpensesService
from src.models.request.individual_expenses import (
    IndividualExpensesBase,
    IndividualExpenses,
)


router = APIRouter()


@router.post("/expenses", response_model=IndividualExpenses)
def create(
    expense: IndividualExpensesBase,
    user: str = Depends(authenticate),
    db: Session = Depends(get_db),
):
    expenses_service: IndividualExpensesService = IndividualExpensesService(db)
    return expenses_service.create(user, expense)
