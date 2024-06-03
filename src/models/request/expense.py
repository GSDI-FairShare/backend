from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from src.models.request.expense_split import ExpenseSplit
from src.models.data.category import ExpenseCategory
from src.models.data.currency import CurrencyType


class ExpenseSplitUser(BaseModel):
    user_id: int
    percentage: float


class ExpenseBase(BaseModel):
    amount: float
    description: str
    category: Optional[ExpenseCategory] = None
    currency: CurrencyType
    date: date
    splits: Optional[List[ExpenseSplitUser]] = None


class ExpenseCreate(ExpenseBase):
    created_by: int
    group_id: int


class ExpenseUpdate(ExpenseBase):
    pass


class Expense(BaseModel):
    id: int
    created_by: int
    group_id: int
    amount: float
    description: str
    category: Optional[ExpenseCategory] = None
    currency: CurrencyType
    date: date
    splits: list[ExpenseSplit] = []

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
