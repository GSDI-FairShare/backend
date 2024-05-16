from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class IndividualExpensesBase(BaseModel):
    user_id: int
    date: date
    description: str
    amount: Decimal


class IndividualExpensesCreate(IndividualExpensesBase):
    pass


class IndividualExpenses(IndividualExpensesBase):
    id: int

    class Config:
        from_attributes = True
