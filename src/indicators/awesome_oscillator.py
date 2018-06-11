from . import sma
from .indicator import Indicator
import ast


class AwesomeOscillator(Indicator):
    def __init__(self, data_array_class, high_period, low_period, time_limits):
        self._sma_a = sma.SMA(low_period)
        self._sma_b = sma.SMA(high_period)
        self._awesome_oscillator = []
        super().__init__(data_array_class, time_limits)

    def update_data_arrays(self):
        mid_point = (self._data.high[-1] + self._data.low[-1]) / 2
        point1 = self._sma_a.update_data_arrays(mid_point)
        point2 = self._sma_b.update_data_arrays(mid_point)
        self._awesome_oscillator.append(point2 - point1)
        super().update_data_arrays()

    def __str__(self):
        return "AWS_OSC\t\tlow_period: {}\thigh_period: {}\ttime: {}".\
            format(self._sma_a.period, self._sma_b.period, self._time_limits)

    def has_broken_above(self):
        return True if self._awesome_oscillator[-1] > 0 > self._awesome_oscillator[-2] else False

    def is_below(self):
        return True if self._awesome_oscillator[-1] < 0 else False

    def is_above(self, *args, **kwargs):
        return True if self._awesome_oscillator[-1] > 0 else False

    def has_broken_below(self, *args, **kwargs):
        return True if self._awesome_oscillator[-1] < 0 < self._awesome_oscillator[-2] else False

    def has_moved_down_for(self, num_candles):
        temp = self._awesome_oscillator[-num_candles:]
        return True if all([temp[x + 1] < temp[x] for x in range(len(temp) - 1)]) else False

    def has_moved_up_for(self, num_candles):
        temp = self._awesome_oscillator[-num_candles:]
        return True if all([temp[x + 1] > temp[x] for x in range(len(temp) - 1)]) else False


def get_class_instance(data_class, **kwargs):
    high_period = kwargs.get('high_period', 34)
    low_period = kwargs.get('low_period', 5)
    time_limits = ast.literal_eval(kwargs.get('time_limits', [(17, 19)]))
    return AwesomeOscillator(data_class,
                             high_period=high_period,
                             low_period=low_period,
                             time_limits=time_limits)
