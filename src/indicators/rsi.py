from ..enums.enums import Position, Trend, Option
import numpy as np


class RSI:
    def __init__(self, data_array_class, period=None, upper_limit=None, lower_limit=None, time_limits=[(17, 19)]):
        self._data = data_array_class
        self.period = period
        self._upper_limit = upper_limit
        self._lower_limit = lower_limit
        self._time_limits = time_limits
        self.avg_gain_of_close = []
        self.avg_loss_of_close = []
        self.relative_strength = []
        self.rsi = []
        self._can_trade = False
        self.valid_trading_time = False
        string = "RSI\t\tperiod: {}, upper: {}, lower: {}, time: {}".format(period, upper_limit,
                                                                            lower_limit, time_limits)
        print(string)
        with open('src/logdata/log.txt', 'a') as log_file:
            log_file.write("\n" + string)

    def is_trading_time(self):
        return self.valid_trading_time

    def update_data_arrays(self):
        if len(self._data.close) >= self.period + 2:
            self._can_trade = True
            self.avg_gain_of_close.append(sum(self._data.gain_of_close[-self.period:]) / self.period)
            self.avg_loss_of_close.append(sum(self._data.loss_of_close[-self.period:]) / self.period)
            self.relative_strength.append(
                self.avg_gain_of_close[-1] / self.avg_loss_of_close[-1] if self.avg_loss_of_close[-1] != 0 else 0)
            self.rsi.append(100 - (100 / (1 + self.relative_strength[-1])) if self.avg_loss_of_close[-1] != 0 else 100)
        else:
            self._can_trade = False
            self.avg_gain_of_close.append(np.NaN)
            self.avg_loss_of_close.append(np.NaN)
            self.relative_strength.append(np.NaN)
            self.rsi.append(np.NaN)
        self.valid_trading_time = self._data.time[-1].tm_wday <= 4 \
                                  and any(tup[0] <= self._data.time[-1].tm_hour < tup[1] for tup in self._time_limits)

    def has_broken_out(self):
        if self._can_trade:
            if self.rsi[-1] > self._upper_limit > self.rsi[-2]:
                return Position.JUST_GONE_ABOVE
            elif self.rsi[-1] < self._lower_limit < self.rsi[-2]:
                return Position.JUST_GONE_BELOW
            else:
                return False
        else:
            return None

    def has_come_back_in(self):
        if self._can_trade:
            if self.rsi[-1] < self._upper_limit < self.rsi[-2]:
                return Position.JUST_REENTERED_FROM_ABOVE
            elif self.rsi[-1] > self._lower_limit > self.rsi[-2]:
                return Position.JUST_REENTERED_FROM_BELOW
            else:
                return False
        else:
            return None

    def get_trend(self):
        if self._can_trade:
            if self.rsi[-1] > self.rsi[-2]:
                return Trend.UP
            elif self.rsi[-1] < self.rsi[-2]:
                return Trend.DOWN
            else:
                return Trend.STRAIGHT
        else:
            return None

    def moving_in_direction_for(self, n=5):
        if self._can_trade:
            temp = self.rsi[-n:]
            if all([temp[x + 1] > temp[x] for x in range(len(temp) - 1)]):
                return Trend.UP
            elif all([temp[x + 1] < temp[x] for x in range(len(temp) - 1)]):
                return Trend.DOWN
            else:
                return Trend.STRAIGHT
        else:
            return None

    def is_outside(self):
        if self._can_trade:
            if self.rsi[-1] > self._upper_limit:
                return Position.ABOVE
            elif self.rsi[-1] < self._lower_limit:
                return Position.BELOW
            else:
                return False
        else:
            return None

    def is_inside(self):
        if self._can_trade:
            return True if self._upper_limit > self.rsi[-1] > self._lower_limit else False
        else:
            return None


def get_class_instance(data_class, **kwargs):
    upper_limit = kwargs.get('upper_limit', 70)
    lower_limit = kwargs.get('lower_limit', 30)
    period = kwargs.get('period', 20)
    time_limits = kwargs.get('time_limits', [(17, 19)])
    return RSI(data_class,
               upper_limit=upper_limit,
               lower_limit=lower_limit,
               period=period,
               time_limits=time_limits)
