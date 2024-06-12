from datetime import date
from typing import Optional

from pydantic import BaseModel
from src.models.data.category import ExpenseCategory
from src.models.data.currency import CurrencyType


class IndividualExpensesBase(BaseModel):
    date: date
    description: str
    amount: float
    category: Optional[ExpenseCategory] = None
    currency: CurrencyType = CurrencyType.ARS
    paid: bool = False


class IndividualExpensesCreate(IndividualExpensesBase):
    user_id: int


class IndividualExpenses(IndividualExpensesBase):
    id: int

    class Config:
        from_attributes = True
