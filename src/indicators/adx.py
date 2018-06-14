import ast

from .indicator import Indicator


class ADX(Indicator):
    def __init__(self, data_array_class, period, time_limits=[]):
        self.period = period
        self.true_range_1 = []
        self.plus_dm_1 = []
        self.minus_dm_1 = []
        self.true_range_period = []
        self.plus_dm_period = []
        self.minus_dm_period = []
        self.plus_directional_indicator = []
        self.minus_directional_indicator = []
        self.directional_indicator_diff = []
        self.directional_indicator_sum = []
        self.dx = []
        self.adx = []
        self._can_trade = False
        super().__init__(data_array_class, time_limits)

    def __str__(self):
        return "ADX\t\tperiod: {}, time: {}".format(self.period, self._time_limits)

    def update_data_arrays(self):
        if len(self._data.close) > 1:
            first_close = self._data.close[-2]
            first_low = self._data.low[-2]
            low = self._data.low[-1]
            first_high = self._data.high[-2]
            high = self._data.high[-1]

            self.true_range_1.append(max(high - low, abs(high - first_close), abs(low - first_close)))
            self.plus_dm_1.append(max(high - first_high, 0) if high - first_high > first_low - low else 0)
            self.minus_dm_1.append(max(first_low - low, 0) if first_low - low > high - first_high else 0)

            if len(self._data.close) > self.period:
                self._can_trade = True
                self.true_range_period.append(sum(self.true_range_1[-self.period:]))
                self.plus_dm_period.append(sum(self.plus_dm_1[-self.period:]))
                self.minus_dm_period.append(sum(self.minus_dm_1[-self.period:]))

                self.plus_directional_indicator.append(100 * (self.plus_dm_period[-1] / self.true_range_period[-1]))
                self.minus_directional_indicator.append(100 * (self.minus_dm_period[-1] / self.true_range_period[-1]))

                self.directional_indicator_diff.append(abs(self.plus_directional_indicator[-1] -
                                                           self.minus_directional_indicator[-1]))
                self.directional_indicator_sum.append(self.plus_directional_indicator[-1] +
                                                      self.minus_directional_indicator[-1])

                self.dx.append(100 * (self.directional_indicator_diff[-1] / self.directional_indicator_sum[-1]))
                self.adx.append(sum(self.dx[-self.period:]) / self.period)

        super().update_data_arrays()

    def is_between(self, **kwargs):
        lower = kwargs.get('lower', 20)
        upper = kwargs.get('upper', 80)
        return True if lower < self.adx[-1] < upper else False

    def has_broken_above(self, **kwargs):
        limit = kwargs.get('limit', 80)
        return True if self.adx[-1] > limit > self.adx[-2] else False

    def has_broken_below(self, **kwargs):
        limit = kwargs.get('limit', 20)
        return True if self.adx[-1] < limit < self.adx[-2] else False

    def is_above(self, **kwargs):
        limit = kwargs.get('limit', 80)
        return True if self.adx[-1] > limit else False

    def is_below(self, **kwargs):
        limit = kwargs.get('limit', 20)
        return True if self.adx[-1] < limit else False

    def has_moved_down_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.adx[-num_candles:]
        return True if all([temp[x + 1] < temp[x] for x in range(len(temp) - 1)]) else False

    def has_moved_up_for(self, **kwargs):
        num_candles = kwargs.get('num_candles', 5)
        temp = self.adx[-num_candles:]
        return True if all([temp[x + 1] > temp[x] for x in range(len(temp) - 1)]) else False


def get_class_instance(data_class, **kwargs):
    period = kwargs.get('period', 20)
    time_limits = ast.literal_eval(kwargs.get('time_limits', [(17, 19)]))
    return ADX(data_class,
               period=period,
               time_limits=time_limits)
