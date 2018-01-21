import time


class EMA:
    def __init__(self, period):
        self._all_data = []
        self._ema_values_array = []
        self._period = period
        self._multiplier = 2.0 / float(period + 1.0)

    def add_data_point(self, point):
        self._all_data.append(point)
        if len(self._ema_values_array) > 1:
            temp1 = float(point) * float(self._multiplier)
            temp2 = float(self._ema_values_array[-1]) * float(1.0 - self._multiplier)
            self._ema_values_array.append(temp1 + temp2)
        else:
            self._ema_values_array.append(point)
        return self._ema_values_array[-1]

    def get_ema_array(self):
        return self._ema_values_array

    def get_last_point_ema_array(self):
        return self._ema_values_array[-1]






