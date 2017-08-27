from enum import Enum


class SelectTypes(Enum):
    TOP_AMOUNT = 0
    BY_DAY = 1
    BY_WEEK = 2
    ALL_BUYS = 3
    ALL_SELLS = 4


class StatementType(Enum):
    SELECT = 0
    INSERT = 1
