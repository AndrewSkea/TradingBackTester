from enums.enums import Position, Trend
from functions import mean_deviation
from indicators.sma import SMA
from constants import finalconstants as const
import numpy as np


class CCI:
    def __init__(self, data_array_class):
        self._data = data_array_class
        self.period = const.cci_period
        self._upper_limit = const.cci_upper_limit
        self._lower_limit = -const.cci_lower_limit
        self._constant = const.cci_constant
        self.typical_price_sma = SMA(self.period)
        self.mean_deviation_typical_price = []
        self.cci = []
        self._can_trade = False

    def update_data_arrays(self):
        if len(self._data.close) >= self.period:
            self._can_trade = True
            self.typical_price_sma.add_data_point(self._data.typical_price[-1])
            self.mean_deviation_typical_price.append(mean_deviation.calculate_mean_deviation(
                self._data.typical_price[-self.period:],
                self.typical_price_sma.get_sma_array()[-1]))
            self.cci.append((self._data.typical_price[-1] - self.typical_price_sma.get_sma_array()[-1]) /
                            (self._constant * self.mean_deviation_typical_price[-1]))
        else:
            self._can_trade = False
            self.typical_price_sma.add_data_point(np.NaN)
            self.mean_deviation_typical_price.append(np.NaN)
            self.cci.append(np.NaN)

    def has_broken_out(self, back_num_values=1):
        if self._can_trade:
            if self.cci[-back_num_values] > self._upper_limit > self.cci[-back_num_values-1]:
                return Position.JUST_GONE_ABOVE
            elif self.cci[-back_num_values] < self._lower_limit < self.cci[-back_num_values-1]:
                return Position.JUST_GONE_BELOW
            else:
                return False
        else:
            return None

    def has_come_back_in(self):
        if self._can_trade:
            if self.cci[-1] < self._upper_limit < self.cci[-2]:
                return Position.JUST_REENTERED_FROM_ABOVE
            elif self.cci[-1] > self._lower_limit > self.cci[-2]:
                return Position.JUST_REENTERED_FROM_BELOW
            else:
                return False
        else:
            return None

    def get_trend(self):
        if self._can_trade:
            if self.cci[-1] > self.cci[-2]:
                return Trend.UP
            elif self.cci[-1] < self.cci[-2]:
                return Trend.DOWN
            else:
                return Trend.STRAIGHT
        else:
            return None

    def is_outside(self):
        if self._can_trade:
            if self.cci[-1] > self._upper_limit:
                return Position.ABOVE
            elif self.cci[-1] < self._lower_limit:
                return Position.BELOW
            else:
                return False
        else:
            return None

    def is_inside(self):
        if self._can_trade:
            return True if self._upper_limit > self.cci[-1] > self._lower_limit else False
        else:
            return None


