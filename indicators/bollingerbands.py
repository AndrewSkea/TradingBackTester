from statistics import pstdev
from enums.enums import Position, Trend
from indicators import sma
from constants import finalconstants as const
import numpy as np


class BollingerBands:
    def __init__(self, data_array_class):
        # BBAND arrays
        self._data = data_array_class
        self.period = const.bollinger_band_sma_period
        self.stdev_multiplier = const.bollinger_band_stdev_multiplier
        self.middle_band = sma.SMA(self.period)
        self.standard_deviation = []
        self.upper_band = []
        self.lower_band = []
        self.band_width = []
        self._can_trade = False

    def update_data_arrays(self):
        if len(self._data.close) >= self.period:
            self._can_trade = True
            self.middle_band.add_data_point(self._data.close[-1])
            self.standard_deviation.append(pstdev(self._data.close[-self.period:]))
            self.upper_band.append(self.middle_band.get_sma_array()[-1] +
                                   self.stdev_multiplier * self.standard_deviation[-1])
            self.lower_band.append(self.middle_band.get_sma_array()[-1] -
                                   self.stdev_multiplier * self.standard_deviation[-1])
        else:
            self._can_trade = False
            self.standard_deviation.append(np.NaN)
            self.upper_band.append(np.NaN)
            self.lower_band.append(np.NaN)

    def has_broken_out(self):
        if self._can_trade:
            if self._data.close[-1] > self.upper_band[-1] > self._data.close[-2]:
                return Position.JUST_GONE_ABOVE
            elif self._data.close[-1] < self.lower_band[-1] < self._data.close[-2]:
                return Position.JUST_GONE_BELOW
            else:
                return False
        else:
            return None

    def has_come_back_in(self):
        if self._can_trade:
            if self._data.close[-1] < self.upper_band[-1] < self._data.close[-2]:
                return Position.JUST_REENTERED_FROM_ABOVE
            elif self._data.close[-1] > self.lower_band[-1] > self._data.close[-2]:
                return Position.JUST_REENTERED_FROM_BELOW
            else:
                return False
        else:
            return None

    def get_trend(self):
        if self._can_trade:
            if self._data.close[-1] > self._data.close[-2]:
                return Trend.UP
            elif self._data.close[-1] < self._data.close[-2]:
                return Trend.DOWN
            else:
                return Trend.STRAIGHT
        else:
            return None

    def is_outside(self):
        if self._can_trade:
            if self._data.close[-1] > self.upper_band[-1]:
                return Position.ABOVE
            elif self._data.close[-1] < self.lower_band[-1]:
                return Position.BELOW
            else:
                return False
        else:
            return None

    def is_inside(self):
        if self._can_trade:
            return True if self.upper_band[-1] > self._data.close[-1] > self.lower_band[-1] else False
        else:
            return None

