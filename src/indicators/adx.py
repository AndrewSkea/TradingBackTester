from enums.enums import Position, Trend, Strength


class ADX:
    def __init__(self, data_array_class, period, time_limits=[]):
        self._time_limits = time_limits
        self._data = data_array_class
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
        self.valid_trading_time = False
        string = "ADX\t\tperiod: {}, time: {}".format(period, time_limits)
        print(string)
        with open('src/logdata/log.txt', 'a') as log_file:
            log_file.write("\n" + string)

    def is_trading_time(self):
        return self.valid_trading_time

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

        self.valid_trading_time = self._data.time[-1].tm_wday <= 4 and any(
            tup[0] <= self._data.time[-1].tm_hour < tup[1] for tup in self._time_limits)

    def get_strength_value(self):
        if self._can_trade:
            return self.adx[-1]
        return 0

    def get_strength_of_trend(self):
        if self._can_trade:
            if self.adx[-1] < 20:
                return Strength.WEAK
            elif 20 <= self.adx[-1] < 30:
                return Strength.MILD
            elif 30 <= self.adx[-1] < 50:
                return Strength.STRONG
            elif 50 <= self.adx[-1] < 100:
                return Strength.VERY_STRONG
        return 0


def get_class_instance(data_class, **kwargs):
    period = kwargs.get('period', 20)
    time_limits = kwargs.get('time_limits', [(17, 19)])
    return ADX(data_class,
               period=period,
               time_limits=time_limits)
