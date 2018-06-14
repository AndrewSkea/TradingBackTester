import ast
from statistics import pstdev
from .indicator import Indicator
from . import sma
import numpy as np


class BollingerBands(Indicator):
    def __init__(self, data_array_class, period, upper_stdev_multiplier, lower_stdev_multiplier, time_limits):
        self.period = period
        self.lower_stdev_multiplier = lower_stdev_multiplier
        self.upper_stdev_multiplier = upper_stdev_multiplier
        self.middle_band = sma.SMA(self.period)
        self.standard_deviation = []
        self.upper_band = []
        self.lower_band = []
        self.band_width = []
        self._can_trade = False
        super().__init__(data_array_class, time_limits)

    def __str__(self):
        return "BBAND\tperiod: {}, lower_stdev_multiplier: {}, upper_stdev_multiplier: {}, time: {}". \
            format(self.period, self.lower_stdev_multiplier, self.upper_stdev_multiplier, self._time_limits)
    
    def update_data_arrays(self):
        if len(self._data.close) >= self.period:
            self._can_trade = True
            self.middle_band.update_data_arrays(self._data.close[-1])
            self.standard_deviation.append(pstdev(self._data.close[-self.period:]))
            self.upper_band.append(self.middle_band.get_sma_array()[-1] +
                                   self.upper_stdev_multiplier * self.standard_deviation[-1])
            self.lower_band.append(self.middle_band.get_sma_array()[-1] -
                                   self.lower_stdev_multiplier * self.standard_deviation[-1])
            self.band_width.append(self.upper_band[-1] - self.lower_band[-1])
        else:
            self._can_trade = False
            self.standard_deviation.append(np.NaN)
            self.upper_band.append(np.NaN)
            self.lower_band.append(np.NaN)
        
        super().update_data_arrays()

    def has_broken_above(self, **kwargs):
        return True if self._data.close[-1] > self.upper_band[-1] > self._data.close[-2] else False

    def has_come_back_in_from_above(self, **kwargs):
        return True if self._data.close[-1] < self.upper_band[-1] < self._data.close[-2] else False

    def is_below(self, **kwargs):
        return True if self._data.close[-1] < self.lower_band[-1] else False

    def is_between(self, **kwargs):
        return True if self.lower_band[-1] < self._data.close[-1] < self.upper_band[-1] else False

    def has_come_back_in_from_below(self, **kwargs):
        return True if self._data.close[-1] > self.lower_band[-1] > self._data.close[-2] else False

    def is_above(self, **kwargs):
        return True if self._data.close[-1] > self.upper_band[-1] else False

    def has_broken_below(self, **kwargs):
        return True if self._data.close[-1] < self.lower_band[-1] < self._data.close[-2] else False

    def has_moved_down_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.middle_band.get_sma_array()[-num_candles:]
        return True if all([temp[x + 1] < temp[x] for x in range(len(temp) - 1)]) else False

    def has_moved_up_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.middle_band.get_sma_array()[-num_candles:]
        return True if all([temp[x + 1] > temp[x] for x in range(len(temp) - 1)]) else False


def get_class_instance(data_class, **kwargs):
    upper_stdev_multiplier = kwargs.get('upper_stdev_multiplier', 2)
    lower_stdev_multiplier = kwargs.get('lower_stdev_multiplier', 2)
    period = kwargs.get('period', 20)
    time_limits = ast.literal_eval(kwargs.get('time_limits', [(17, 19)]))
    return BollingerBands(data_class,
                          upper_stdev_multiplier=upper_stdev_multiplier,
                          lower_stdev_multiplier=lower_stdev_multiplier,
                          period=period,
                          time_limits=time_limits)
