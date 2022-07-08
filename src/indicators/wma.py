import ast

from .indicator import Indicator


class WMA(Indicator):
    def __init__(self, period, data_array_class=None, time_limits=None):
        self._all_data = []
        self.wma = []
        self.period = period
        super().__init__(data_array_class, time_limits)

    def update_data_arrays(self, point=None):
        point = self._data.close[-1] if point is None else point
        self._all_data.append(point)
        if len(self._all_data) > self.period:
            division_num = sum(range(self.period + 1))
            temp_array = []
            for i in range(self.period):
                temp_array.append((self._all_data[-(self.period - i)] * (self.period - i)) / division_num)
            self.wma.append(sum(temp_array))
            return self.wma[-1]

    def get_wma_array(self):
        return self.wma

    def __str__(self):
        return "WMA\t\tperiod: {}\ttime: {}".format(self.period, self._time_limits)

    def has_moved_down_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.wma[-num_candles:]
        return True if all([temp[x + 1] < temp[x] for x in range(len(temp) - 1)]) else False

    def has_moved_up_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.wma[-num_candles:]
        return True if all([temp[x + 1] > temp[x] for x in range(len(temp) - 1)]) else False

def get_class_instance(data_class, **kwargs):
    period = kwargs.get('period', 20)
    time_limits = ast.literal_eval(kwargs.get('time_limits', [(17, 19)]))
    return WMA(data_array_class=data_class,
               period=period,
               time_limits=time_limits)
