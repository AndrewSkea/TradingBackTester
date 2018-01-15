class WMA:
    def __init__(self, period):
        self._all_data = []
        self._wma_values_array = []
        self._period = period

    def add_data_point(self, point):
        self._all_data.append(point)
        division_num = sum(range(self._period + 1))
        try:
            temp_array = []
            for i in range(self._period):
                temp_array.append((self._all_data[-(self._period - i)] * (self._period - i))/division_num)
            self._wma_values_array.append(sum(temp_array))
            return self._wma_values_array[-1]
        except IndexError:
            self._wma_values_array.append(point)

    def get_wma_array(self):
        return self._wma_values_array
