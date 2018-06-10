from .indicator import Indicator
from ..functions import mean_deviation
from .sma import SMA
import numpy as np
import ast


class CCI(Indicator):
    def __init__(self, data_array_class, upper_limit, lower_limit, period, time_limits):
        self.period = period
        self._upper_limit = upper_limit
        self._lower_limit = -abs(lower_limit)
        self.typical_price_sma = SMA(self.period)
        self.mean_deviation_typical_price = []
        self.cci = []
        self._can_trade = False
        self.valid_trading_time = False
        super().__init__(data_array_class, time_limits)

    def __str__(self):
        return "CCI\t\tperiod: {}, upper: {}, lower: {}, time: {}".format(self.period, self._upper_limit,
                                                                          self._lower_limit, self._time_limits)

    def update_data_arrays(self):
        if len(self._data.close) >= self.period:
            self._can_trade = True
            self.typical_price_sma.add_data_point(self._data.typical_price[-1])
            self.mean_deviation_typical_price.append(mean_deviation.calculate_mean_deviation(
                self._data.typical_price[-self.period:],
                self.typical_price_sma.get_sma_array()[-1]))
            self.cci.append((self._data.typical_price[-1] - self.typical_price_sma.get_sma_array()[-1]) /
                            (0.015 * self.mean_deviation_typical_price[-1]))
        else:
            self._can_trade = False
            self.typical_price_sma.add_data_point(np.NaN)
            self.mean_deviation_typical_price.append(np.NaN)
            self.cci.append(np.NaN)

        super().update_data_arrays()

    def has_moved_down_for(self):
        temp = self.cci[-5:]
        return True if all([temp[x + 1] < temp[x] for x in range(len(temp) - 1)]) else False

    def has_broken_above(self):
        return True if self.cci[-1] > self._upper_limit > self.cci[-2] else False

    def has_come_back_in_from_below(self):
        return True if self.cci[-1] > self._lower_limit > self.cci[-2] else False

    def has_come_back_in_from_above(self):
        return True if self.cci[-1] < self._upper_limit < self.cci[-2] else False

    def has_broken_below(self):
        return True if self.cci[-1] < self._lower_limit < self.cci[-2] else False

    def is_above(self):
        return True if self.cci[-1] > self._upper_limit else False

    def has_moved_up_for(self):
        temp = self.cci[-5:]
        return True if all([temp[x + 1] > temp[x] for x in range(len(temp) - 1)]) else False

    def is_below(self):
        return True if self.cci[-1] < self._lower_limit else False

    def is_inside(self):
        return True if self._upper_limit > self.cci[-1] > self._lower_limit else False


def get_class_instance(data_class, **kwargs):
    upper_limit = kwargs.get('upper_limit', 100)
    lower_limit = kwargs.get('lower_limit', 100)
    period = kwargs.get('period', 20)
    time_limits = ast.literal_eval(kwargs.get('time_limits', [(17, 19)]))
    return CCI(data_class,
               upper_limit=upper_limit,
               lower_limit=lower_limit,
               period=period,
               time_limits=time_limits)
