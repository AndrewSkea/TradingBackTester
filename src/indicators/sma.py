import numpy as np


class SMA:
    def __init__(self, period):
        self._all_data = []
        self._sma_values_array = []
        self._period = period

    def add_data_point(self, point):
        self._all_data.append(float(point or np.NaN))
        self._sma_values_array.append(sum(self._all_data[-self._period:]) / self._period)
        return self._sma_values_array[-1]

    def get_sma_array(self):
        return self._sma_values_array