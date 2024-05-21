from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class ExpenseBase(BaseModel):
    group_id: int
    amount: Decimal
    description: str
    date: datetime


class ExpenseCreate(ExpenseBase):
    created_by: int


class ExpenseUpdate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int

    class Config:
        from_attributes = True
