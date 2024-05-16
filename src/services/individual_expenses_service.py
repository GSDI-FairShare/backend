from sqlalchemy.orm import Session
from src.repository.individual_expenses_repository import IndividualExpensesRepository
from src.services.user_service import UserService
from src.models.request.individual_expenses import IndividualExpensesBase
from src.models.request.individual_expenses import IndividualExpensesCreate


class IndividualExpensesService:
    def __init__(self, db: Session):
        self.expenses_repository: IndividualExpensesRepository = (
            IndividualExpensesRepository(db)
        )
        self.user_service: UserService = UserService(db)

    def create(self, email: str, expense: IndividualExpensesBase):
        user_db = self.user_service.find_by_email(email)
        expense_data = expense.model_dump()
        expense_create = IndividualExpensesCreate(**expense_data, user_id=user_db.id)
        return self.expenses_repository.save(expense_create)
