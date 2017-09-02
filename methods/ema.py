from enums import enums


class EMA:
    def __init__(self, all_close_data, period):
        self._all_data = all_close_data
        self._ema_values_array = []
        self._period = period
        self._multiplier = float(2) / float((period + 1))

    def calculate_initial_ema_array(self):
        """
        Calculates the ema pattern of past data
        :return:
        """
        # Gets the first average of the first [period] data points
        self._ema_values_array.append(reduce(lambda x, y: x + y, self._all_data[:self._period]) / self._period)
        for i in range(self._period, len(self._all_data), 1):
            current_ema = (self._all_data[i] * self._multiplier +
                           self._ema_values_array[-1] * (1 - self._multiplier))
            self._ema_values_array.append(current_ema)

    def get_result(self):
        _option = enums.Option.BUY
        return _option

    def add_data_point(self, point):
        self._ema_values_array.append(point * self._multiplier + self._ema_values_array[-1] * (1 - self._multiplier))
        return self._ema_values_array[-1]

    def get_ema_array(self):
        return self._ema_values_array






