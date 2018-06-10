import numpy as np


class EMA:
    def __init__(self, period):
        self._all_data = []
        self._ema_values_array = []
        self._period = period
        self._multiplier = 2.0 / float(period + 1.0)

    def add_data_point(self, point):
        if not np.isnan(point):
            self._all_data.append(point)
            if len(self._ema_values_array) > 1:
                self._ema_values_array.append((point * self._multiplier) +
                                              (float(self._ema_values_array[-1]) * float(1.0 - self._multiplier)))
            else:
                self._ema_values_array.append(point)
            return self._ema_values_array[-1]
        return None

    def get_ema_array(self):
        return self._ema_values_array if len(self._ema_values_array) > 1 else [234, 324]
