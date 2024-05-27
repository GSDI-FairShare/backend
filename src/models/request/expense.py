from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from decimal import Decimal


class ExpenseSplitUser(BaseModel):
    user_id: int
    percentage: float


class ExpenseBase(BaseModel):
    amount: float
    description: str
    date: date
    splits: Optional[List[ExpenseSplitUser]] = None


class ExpenseCreate(ExpenseBase):
    created_by: int
    group_id: int


class ExpenseUpdate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int
    created_by: int
    group_id: int

    class Config:
        from_attributes = True


# class ExpenseSplitCreate(BaseModel):
#     user_id: int
#     amount: float
#
#
# class ExpenseSplitUpdate(BaseModel):
#     paid: bool
#
#
# class ExpenseResponse(BaseModel):
#     id: int
#     amount: float
#     description: str
#     date: datetime
#     created_by: int
#
#     class Config:
#         from_attributes = True


# class ExpenseSplitResponse(BaseModel):
#     id: int
#     expense_id: int
#     user_id: int
#     amount: float
#     paid: bool
#
#     class Config:
#         from_attributes = True
