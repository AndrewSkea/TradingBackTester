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
    UP = 0
    DOWN = 1
    STRAIGHT = 2


class Position(Enum):
    ABOVE = 0
    BELOW = 1
    EQUAL = 2
    BETWEEN = 3


class Indicators(Enum):
    SMA = 0
    EMA = 1
    WMA = 2
    CCI = 3
    MACD = 4
    BBAND = 5
    AO = 6
    CUST_1 = 7
    PC = 8
    RSI = 9
    STOCHOSC = 10
    TYPRI = 11
    CUST_2 = 12
    CUST_3 = 13
