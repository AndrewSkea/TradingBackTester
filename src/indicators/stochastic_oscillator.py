from ..enums.enums import Position


class StochasticOscillator:
    def __init__(self, data_array_class, k_period, d_period, upper_limit=80, lower_limit=20, time_limits=[]):
        self._lower_limit = lower_limit
        self._upper_limit = upper_limit
        self._time_limits = time_limits
        self._data = data_array_class
        self.d_period = d_period
        self.k_period = k_period
        self.stoch_ar = []
        self.sma_stoch_ar = []
        self.valid_trading_time = False

    def is_trading_time(self):
        return self.valid_trading_time

    def update_data_arrays(self):
        if len(self._data.close) > self.k_period:
            self.stoch_ar.append(100 * (self._data.close[-1] - min(self._data.low[-self.k_period:])) /
                                 (max(self._data.high[-self.k_period:]) - min(self._data.low[-self.k_period:])))
            self.sma_stoch_ar.append(((sum(self.stoch_ar[-self.d_period:])) / self.d_period))
            self.valid_trading_time = self._data.time[-1].tm_wday <= 4 and any(
                tup[0] <= self._data.time[-1].tm_hour < tup[1] for tup in self._time_limits)

    def has_crossed_over(self):
        if len(self.stoch_ar) > 2:
            if self.stoch_ar[-1] > self.sma_stoch_ar[-1] > self.stoch_ar[-2]:
                return Position.JUST_GONE_ABOVE
            elif self.stoch_ar[-1] < self.sma_stoch_ar[-1] < self.stoch_ar[-2]:
                return Position.JUST_GONE_BELOW
        return None

    def is_outside(self):
        if len(self.stoch_ar) > 0:
            if self.stoch_ar[-1] > self._upper_limit:
                return Position.ABOVE
            elif self.stoch_ar[-1] < self._lower_limit:
                return Position.BELOW
        return None


def get_class_instance(data_class, **kwargs):
    upper_limit = kwargs.get('upper_limit', 80)
    lower_limit = kwargs.get('lower_limit', 20)
    k_period = kwargs.get('k_period', 20)
    d_period = kwargs.get('d_period', 20)
    time_limits = kwargs.get('time_limits', [(17, 19)])
    return StochasticOscillator(data_class,
                                upper_limit=upper_limit,
                                lower_limit=lower_limit,
                                k_period=k_period,
                                d_period=d_period,
                                time_limits=time_limits)
