import ast

import numpy as np

from .indicator import Indicator


class SMA(Indicator):
    def __init__(self, period, data_array_class=None, time_limits=None):
        self._data = data_array_class
        self._time_limits = time_limits
        self._all_data = []
        self.sma = []
        self.period = period
        super().__init__(data_array_class, time_limits)

    def __str__(self):
        return "SMA\t\tperiod: {}\ttime: {}".format(self.period, self._time_limits)

    def update_data_arrays(self, point=None):
        if point is not None:
            self._all_data.append(float(point or np.NaN))
            self.sma.append(sum(self._all_data[-self.period:]) / self.period)
        else:
            self.sma.append(sum(self._data.close[-self.period:]) / self.period)
        super().update_data_arrays()
        return self.sma[-1]

    def get_sma_array(self):
        return self.sma

    def has_moved_down_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.sma[-num_candles:]
        return True if all([temp[x + 1] < temp[x] for x in range(len(temp) - 1)]) else False

    def has_moved_up_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.sma[-num_candles:]
        return True if all([temp[x + 1] > temp[x] for x in range(len(temp) - 1)]) else False


def get_class_instance(data_class, **kwargs):
    period = kwargs.get('period', 20)
    time_limits = ast.literal_eval(kwargs.get('time_limits', [(17, 19)]))
    return SMA(data_array_class=data_class,
               period=period,
               time_limits=time_limits)