from pydantic import BaseModel
from decimal import Decimal


class ExpenseSplitBase(BaseModel):
    expense_id: int
    user_id: int
    percentage: Decimal
    paid: bool


class ExpenseSplitCreate(ExpenseSplitBase):
    pass


class ExpenseSplitUpdate(ExpenseSplitBase):
    pass


class ExpenseSplit(ExpenseSplitBase):
    id: int

    class Config:
        from_attributes = True
