from enum import Enum


class ExpenseCategory(str, Enum):
    FOOD = "comida"
    TRANSPORT = "transporte"
    SHOPPING = "shopping"
    ENTERTAINMENT = "entretenimiento"
    OTHER = "otro"
