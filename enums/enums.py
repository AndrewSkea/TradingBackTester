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


class Option(Enum):
    SELL = 0
    BUY = 1
    DRAW = 2
    NO_TRADE = 3


class Trend(Enum):
    UP = 0,
    DOWN = 1,
    STRAIGHT = 2


class Position(Enum):
    ABOVE = 0,
    BELOW = 1,
    EQUAL = 2
