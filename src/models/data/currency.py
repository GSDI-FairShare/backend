from enum import Enum


class CurrencyType(str, Enum):
    USD = "USD"
    EUR = "EUR"
    MXN = "MXN"
    BRL = "BRL"
    ARS = "ARS"
