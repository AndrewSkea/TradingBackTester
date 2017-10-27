from enums import enums


class SMA:
    def __init__(self, all_data, period):
        self._all_data = all_data
        self._sma_values_array = []
        self._period = period

    def calculate_initial_sma_array(self):
        """
        Calculates the sma pattern of past data
        :return:
        """
        # Gets the SMA of all the data
        for i in range(self._period, len(self._all_data), 1):
            self._sma_values_array.append(round(sum(self._all_data[i-self._period:i]) / self._period, 10))

    def get_result(self):
        _option = enums.Option.BUY
        return _option

    def add_data_point(self, point):
        self._all_data.append(point)
        self._sma_values_array.append(round(sum(self._all_data[-self._period:]) / self._period, 10))
        return self._sma_values_array[-1]

    def get_sma_array(self):
        return self._sma_values_array
