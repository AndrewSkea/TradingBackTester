import ast

from .indicator import Indicator
import numpy as np


class RSI(Indicator):
    def __init__(self, data_array_class, period, upper_limit, lower_limit, time_limits):
        self._data = data_array_class
        self.period = period
        self._upper_limit = upper_limit
        self._lower_limit = lower_limit
        self._time_limits = time_limits
        self.avg_gain_of_close = []
        self.avg_loss_of_close = []
        self.relative_strength = []
        self.rsi = []
        self._can_trade = False
        super().__init__(data_array_class, time_limits)

    def __str__(self):
        return "RSI\t\tperiod: {}, upper: {}, lower: {}, time: {}".format(self.period, self._upper_limit,
                                                                          self._lower_limit, self._time_limits)

    def update_data_arrays(self):
        if len(self._data.close) >= self.period + 2:
            self._can_trade = True
            self.avg_gain_of_close.append(sum(self._data.gain_of_close[-self.period:]) / self.period)
            self.avg_loss_of_close.append(sum(self._data.loss_of_close[-self.period:]) / self.period)
            self.relative_strength.append(
                self.avg_gain_of_close[-1] / self.avg_loss_of_close[-1] if self.avg_loss_of_close[-1] != 0 else 0)
            self.rsi.append(100 - (100 / (1 + self.relative_strength[-1])) if self.avg_loss_of_close[-1] != 0 else 100)
        else:
            self._can_trade = False
            self.avg_gain_of_close.append(np.NaN)
            self.avg_loss_of_close.append(np.NaN)
            self.relative_strength.append(np.NaN)
            self.rsi.append(np.NaN)

        super().update_data_arrays()

    def has_moved_down_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.rsi[-num_candles:]
        return True if all([temp[x + 1] < temp[x] for x in range(len(temp) - 1)]) else False

    def has_broken_above(self, **kwargs):
        return True if self.rsi[-1] > self._upper_limit > self.rsi[-2] else False

    def has_come_back_in_from_below(self, **kwargs):
        return True if self.rsi[-1] > self._lower_limit > self.rsi[-2] else False

    def has_come_back_in_from_above(self, **kwargs):
        return True if self.rsi[-1] < self._upper_limit < self.rsi[-2] else False

    def has_broken_below(self, **kwargs):
        return True if self.rsi[-1] < self._lower_limit < self.rsi[-2] else False

    def is_above(self, **kwargs):
        return True if self.rsi[-1] > self._upper_limit else False

    def has_moved_up_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.rsi[-num_candles:]
        return True if all([temp[x + 1] > temp[x] for x in range(len(temp) - 1)]) else False

    def is_below(self, **kwargs):
        return True if self.rsi[-1] < self._lower_limit else False

    def is_between(self, **kwargs):
        return True if self._upper_limit > self.rsi[-1] > self._lower_limit else False


def get_class_instance(data_class, **kwargs):
    upper_limit = kwargs.get('upper_limit', 70)
    lower_limit = kwargs.get('lower_limit', 30)
    period = kwargs.get('period', 20)
    time_limits = ast.literal_eval(kwargs.get('time_limits', [(17, 19)]))
    return RSI(data_class,
               upper_limit=upper_limit,
               lower_limit=lower_limit,
               period=period,
               time_limits=time_limits)
