from pydantic import BaseModel


class ExpenseSplitBase(BaseModel):
    expense_id: int
    user_id: int
    amount: float
    percentage: float
    paid: bool


class ExpenseSplitCreate(ExpenseSplitBase):
    pass


class ExpenseSplitUpdate(ExpenseSplitBase):
    pass


class ExpenseSplit(ExpenseSplitBase):
    id: int

    class Config:
        from_attributes = True
