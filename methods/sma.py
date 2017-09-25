from enums import enums


class SMA:
    def __init__(self, all_close_data, period):
        self._all_data = all_close_data
        self._sma_values_array = []
        self._period = period

    def calculate_initial_sma_array(self):
        """
        Calculates the sma pattern of past data
        :return:
        """
        # Gets the first average of the first [period] data points
        self._sma_values_array.append(reduce(lambda x, y: x + y, self._all_data[:self._period]) / self._period)
        for i in range(self._period, len(self._all_data), 1):
            current_sma = (self._all_data[i] + self._sma_values_array[-1])
            self._sma_values_array.append(current_sma)

    def get_result(self):
        _option = enums.Option.BUY
        return _option

    def add_data_point(self, point):
        self._sma_values_array.append(point + self._sma_values_array[-1])
        return self._sma_values_array[-1]

    def get_sma_array(self):
        return self._sma_values_array