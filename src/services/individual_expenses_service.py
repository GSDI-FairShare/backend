from sqlalchemy.orm import Session
from src.repository.individual_expenses_repository import IndividualExpensesRepository
from src.models.request.individual_expenses import IndividualExpensesCreate


class IndividualExpensesService:
    def __init__(self, db: Session):
        self.individual_expenses_repository: IndividualExpensesRepository = (
            IndividualExpensesRepository(db)
        )

    def create(self, expense: IndividualExpensesCreate):
        return self.individual_expenses_repository.save(expense)
