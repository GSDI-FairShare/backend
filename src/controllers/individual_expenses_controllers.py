from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.auth.authenticate import authenticate
from src.services.individual_expenses_service import IndividualExpensesService

from src.repository.individual_expenses_repository import IndividualExpensesRepository
from src.services.user_service import UserService
from src.models.request.individual_expenses import (
    IndividualExpensesBase,
    IndividualExpenses,
)

router = APIRouter()


# Dependencia para obtener el servicio
def get_individual_expenses_service(
    db: Session = Depends(get_db),
) -> IndividualExpensesService:
    expenses_repository = IndividualExpensesRepository(db)
    user_service = UserService(db)
    return IndividualExpensesService(expenses_repository, user_service)


@router.post("/expenses", response_model=IndividualExpenses)
def create_expense(
    expense: IndividualExpensesBase,
    user: str = Depends(authenticate),
    expenses_service: IndividualExpensesService = Depends(
        get_individual_expenses_service
    ),
):
    return expenses_service.create(user, expense)


@router.get("/expenses", response_model=list[IndividualExpenses])
def get_expenses(
    user: str = Depends(authenticate),
    expenses_service: IndividualExpensesService = Depends(
        get_individual_expenses_service
    ),
):
    return expenses_service.get_expenses(user)
