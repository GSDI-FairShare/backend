from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.models.data.expense import Expense
from src.models.request.expense import (
    ExpenseBase,
    ExpenseCreate,
    ExpenseUpdate,
)
from src.models.request.expense_split import ExpenseSplitBase
from src.models.request.expense_split import ExpenseSplitCreate
from src.repository.expense_repository import ExpenseRepository
from src.services.expense_split_service import ExpenseSplitService
from src.services.group_members_service import GroupMembersService
from src.services.group_service import GroupService
from src.services.expense_split_service import create_expense_split_service
from src.services.group_members_service import create_group_members_service
from src.services.group_service import create_group_service


class ExpenseService:
    def __init__(
        self,
        expense_repository: ExpenseRepository,
        group_service: GroupService,
        group_members_service: GroupMembersService,
        expense_split_service: ExpenseSplitService,
    ):
        self.expense_repository = expense_repository
        self.group_service = group_service
        self.group_members_service = group_members_service
        self.expense_split_service = expense_split_service

    def create_expense(
        self, user_id: int, group_id: int, expense: ExpenseBase
    ) -> Expense:
        group = self.group_service.get_group(group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group with id {group_id} not found",
            )
        expenseData = expense.model_dump()
        expenseData["created_by"] = user_id
        expenseData["group_id"] = group_id
        new_expense = self.expense_repository.save(ExpenseCreate(**expenseData))
        if not expense.splits:
            members = self.group_members_service.get_group_members_by_group_id(group_id)
            if len(members) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Group has no members",
                )
            split_amount = expense.amount / len(members)
            for member in members:
                split_data = {
                    "expense_id": new_expense.id,
                    "user_id": member.user_id,
                    "amount": split_amount,
                    "percentage": 100 / len(members),
                    "paid": False,
                }
                self.expense_split_service.create_split_expense(
                    ExpenseSplitCreate(**split_data)
                )
        else:
            for split in expense.splits:
                split_data = {
                    "expense_id": new_expense.id,
                    "user_id": split.user_id,
                    "amount": expense.amount * split.percentage / 100,
                    "percentage": split.percentage,
                    "paid": False,
                }
                self.expense_split_service.create_split_expense(
                    ExpenseSplitCreate(**split_data)
                )
        return new_expense

    def get_expenses(self, user_id: int, group_id: int) -> List[Expense]:
        group = self.group_service.get_group(group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group with id {group_id} not found",
            )
        if not self.group_members_service.is_user_member_of_group(user_id, group_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of this group",
            )
        return self.expense_repository.find_by_group_id(group_id)


def create_expense_service(session: Session) -> ExpenseService:
    return ExpenseService(
        expense_repository=ExpenseRepository(session),
        group_service=create_group_service(session),
        group_members_service=create_group_members_service(session),
        expense_split_service=create_expense_split_service(session),
    )
