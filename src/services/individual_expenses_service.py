from sqlalchemy.orm import Session
from src.repository.individual_expenses_repository import IndividualExpensesRepository
from src.services.user_service import UserService
from src.models.request.individual_expenses import (
    IndividualExpensesBase,
    IndividualExpensesCreate,
)


class IndividualExpensesService:
    def __init__(
        self,
        expenses_repository: IndividualExpensesRepository,
        user_service: UserService,
    ):
        self.expenses_repository = expenses_repository
        self.user_service = user_service

    def create(self, email: str, expense: IndividualExpensesBase):
        user_db = self.user_service.find_by_email(email)
        expense_data = expense.model_dump()
        expense_create = IndividualExpensesCreate(**expense_data, user_id=user_db.id)
        return self.expenses_repository.save(expense_create)

    def get_expenses(self, email: str):
        user_db = self.user_service.find_by_email(email)
        return self.expenses_repository.find_by_user_id(user_db.id)


# Factory function to create an instance of the service
def create_individual_expenses_service(db: Session) -> IndividualExpensesService:
    expenses_repository = IndividualExpensesRepository(db)
    user_service = UserService(db)
    return IndividualExpensesService(expenses_repository, user_service)
