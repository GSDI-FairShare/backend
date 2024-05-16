from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class IndividualExpensesBase(BaseModel):
    date: date
    description: str
    amount: Decimal


class IndividualExpensesCreate(IndividualExpensesBase):
    user_id: int


class IndividualExpenses(IndividualExpensesBase):
    id: int

    class Config:
        from_attributes = True
