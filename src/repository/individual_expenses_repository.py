from sqlalchemy.orm import Session

from src.models.data.user import User

from src.models.data.individual_expenses import IndividualExpenses

from src.models.request.individual_expenses import IndividualExpensesCreate


class IndividualExpensesRepository:
    def __init__(self, sess: Session):
        self.db: Session = sess

    def save(self, expense: IndividualExpensesCreate):
        expense = IndividualExpenses(
            user_id=expense.user_id,
            amount=expense.amount,
            description=expense.description,
            date=expense.date,
        )
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense
