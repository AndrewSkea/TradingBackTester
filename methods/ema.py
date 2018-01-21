from enums import enums
import functools


class EMA:
    def __init__(self, all_close_data, period):
        self._all_data = list(all_close_data)
        self._ema_values_array = []
        self._period = period
        self._multiplier = float(2) / float((period + 1))

    def add_data_point(self, point):
        self._all_data.append(point)
        try:
            self._ema_values_array.append(point * self._multiplier + self._ema_values_array[-1] * (1 - self._multiplier))
            return self._ema_values_array[-1]
        except IndexError:
            self._ema_values_array.append(point)

    def get_ema_array(self):
        return self._ema_values_array






