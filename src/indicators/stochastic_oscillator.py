import ast

from .indicator import Indicator


class StochasticOscillator(Indicator):
    def __init__(self, data_array_class, k_period, d_period, upper_limit, lower_limit, time_limits):
        self._lower_limit = lower_limit
        self._upper_limit = upper_limit
        self._time_limits = time_limits
        self._data = data_array_class
        self.d_period = d_period
        self.k_period = k_period
        self.stoch_ar = []
        self.sma_stoch_ar = []
        super().__init__(data_array_class, time_limits)

    def __str__(self):
        return "STOCH\t\tk_period: {}, d_period: {}, upper: {}, lower: {}, time: {}".\
            format(self.k_period, self.d_period, self._upper_limit, self._lower_limit, self._time_limits)

    def update_data_arrays(self):
        if len(self._data.close) > self.k_period:
            self.stoch_ar.append(100 * (self._data.close[-1] - min(self._data.low[-self.k_period:])) /
                                 (max(self._data.high[-self.k_period:]) - min(self._data.low[-self.k_period:])))
            self.sma_stoch_ar.append(((sum(self.stoch_ar[-self.d_period:])) / self.d_period))

        super().update_data_arrays()

    def has_broken_above(self, **kwargs):
        return True if self.sma_stoch_ar[-1] > self._upper_limit > self.sma_stoch_ar[-2] else False

    def has_come_back_in_from_above(self, **kwargs):
        return True if self.sma_stoch_ar[-1] < self._upper_limit < self.sma_stoch_ar[-2] else False

    def is_below(self, **kwargs):
        return True if self.sma_stoch_ar[-1] < self._lower_limit else False

    def is_between(self, **kwargs):
        return True if self._lower_limit < self.sma_stoch_ar[-1] < self._upper_limit else False

    def has_come_back_in_from_below(self, **kwargs):
        return True if self.sma_stoch_ar[-1] > self._lower_limit > self.sma_stoch_ar[-2] else False

    def is_above(self, **kwargs):
        return True if self.sma_stoch_ar[-1] < self._upper_limit else False

    def has_broken_below(self, **kwargs):
        return True if self.sma_stoch_ar[-1] < self._lower_limit < self.sma_stoch_ar[-2] else False

    def has_moved_down_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.sma_stoch_ar[-num_candles:]
        return True if all([temp[x + 1] < temp[x] for x in range(len(temp) - 1)]) else False

    def has_moved_up_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.sma_stoch_ar[-num_candles:]
        return True if all([temp[x + 1] > temp[x] for x in range(len(temp) - 1)]) else False


def get_class_instance(data_class, **kwargs):
    upper_limit = kwargs.get('upper_limit', 80)
    lower_limit = kwargs.get('lower_limit', 20)
    k_period = kwargs.get('k_period', 20)
    d_period = kwargs.get('d_period', 20)
    time_limits = ast.literal_eval(kwargs.get('time_limits', [(17, 19)]))
    return StochasticOscillator(data_class,
                                upper_limit=upper_limit,
                                lower_limit=lower_limit,
                                k_period=k_period,
                                d_period=d_period,
                                time_limits=time_limits)
