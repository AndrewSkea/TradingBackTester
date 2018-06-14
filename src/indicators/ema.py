import ast

import numpy as np

from .indicator import Indicator


class EMA(Indicator):
    def __init__(self, data_array_class, time_limits, period):
        self._all_data = []
        self.ema = []
        self.period = period
        self._multiplier = 2.0 / float(period + 1.0)
        super().__init__(data_array_class, time_limits)

    def update_data_arrays(self, point=None):
        if not np.isnan(point):
            self._all_data.append(point)
            if len(self.ema) > 1:
                self.ema.append((point * self._multiplier) +
                                (float(self.ema[-1]) * float(1.0 - self._multiplier)))
            else:
                self.ema.append(point)
            return self.ema[-1]
        return None
        super().update_data_arrays()

    def get_ema_array(self):
        return self.ema if len(self.ema) > 1 else []

    def __str__(self):
        return "EMA\t\tperiod: {}\ttime: {}".format(self.period, self._time_limits)

    def has_moved_down_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.ema[-num_candles:]
        return True if all([temp[x + 1] < temp[x] for x in range(len(temp) - 1)]) else False

    def has_moved_up_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.ema[-num_candles:]
        return True if all([temp[x + 1] > temp[x] for x in range(len(temp) - 1)]) else False


def get_class_instance(data_class, **kwargs):
    period = kwargs.get('period', 20)
    time_limits = ast.literal_eval(kwargs.get('time_limits', [(17, 19)]))
    return EMA(data_array_class=data_class,
               period=period,
               time_limits=time_limits)