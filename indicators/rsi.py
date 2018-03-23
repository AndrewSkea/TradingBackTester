from constants import finalconstants as const
from enums.enums import Position, Trend
import numpy as np


class RSI:
    def __init__(self, data_array_class):
        self._data = data_array_class
        self._constants = const
        self.period = const.rsi_period
        self._upper_limit = const.rsi_upper_limit
        self._lower_limit = const.rsi_lower_limit
        self.avg_gain_of_close = []
        self.avg_loss_of_close = []
        self.relative_strength = []
        self.rsi = []
        self._can_trade = False

    def update_data_arrays(self):
        if len(self._data.close) >= self.period + 2:
            self._can_trade = True
            self.avg_gain_of_close.append(sum(self._data.gain_of_close[-self.period:]) / self.period)
            self.avg_loss_of_close.append(sum(self._data.loss_of_close[-self.period:]) / self.period)
            self.relative_strength.append(self.avg_gain_of_close[-1] / self.avg_loss_of_close[-1])
            self.rsi.append(100-(100/(1+self.relative_strength[-1])) if self.avg_loss_of_close[-1] != 0 else 100)
        else:
            self._can_trade = False
            self.avg_gain_of_close.append(np.NaN)
            self.avg_loss_of_close.append(np.NaN)
            self.relative_strength.append(np.NaN)
            self.rsi.append(np.NaN)

    def has_broken_out(self):
        if self._can_trade:
            if self.rsi[-1] > self._upper_limit > self.rsi[-2]:
                return Position.JUST_GONE_ABOVE
            elif self.rsi[-1] < self._lower_limit < self.rsi[-2]:
                return Position.JUST_GONE_BELOW
            else:
                return False
        else:
            return None

    def has_come_back_in(self):
        if self._can_trade:
            if self.rsi[-1] < self._upper_limit < self.rsi[-2]:
                return Position.JUST_REENTERED_FROM_ABOVE
            elif self.rsi[-1] > self._lower_limit > self.rsi[-2]:
                return Position.JUST_REENTERED_FROM_BELOW
            else:
                return False
        else:
            return None

    def get_trend(self):
        if self._can_trade:
            if self.rsi[-1] > self.rsi[-2]:
                return Trend.UP
            elif self.rsi[-1] < self.rsi[-2]:
                return Trend.DOWN
            else:
                return Trend.STRAIGHT
        else:
            return None

    def is_outside(self):
        if self._can_trade:
            if self.rsi[-1] > self._upper_limit:
                return Position.ABOVE
            elif self.rsi[-1] < self._lower_limit:
                return Position.BELOW
            else:
                return False
        else:
            return None

    def is_inside(self):
        if self._can_trade:
            return True if self._upper_limit > self.rsi[-1] > self._lower_limit else False
        else:
            return None


