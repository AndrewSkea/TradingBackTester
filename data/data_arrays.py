from statistics import pstdev
import numpy as np


class DataArrays:
    def __init__(self, period):
        """
        These are data arrays that have a period of self.period. If you want something different, you will have to
        overwrite it in your own class
        """
        self.period = period
        # Base Arrays
        self.time = []
        self.open = []
        self.high = []
        self.low = []
        self.close = []
        self.change_of_close = []
        self.gain_of_close = []
        self.loss_of_close = []
        self.typical_price = []
        # MA arrays
        self.close_sma = []
        self.close_ema = []
        self.close_wma = []
        # TradingTime Boolean
        self.valid_trading_time = True

    def add_data(self, time_value, open_value, high_value, low_value, close_value):
        self.time.append(time_value)
        self.open.append(open_value)
        self.high.append(high_value)
        self.low.append(low_value)
        self.close.append(close_value)
        self.typical_price.append((close_value + high_value + low_value) / 3)

        if self.time[-1].tm_wday <= 4 and 17 <= self.time[-1].tm_hour < 19:
            self.valid_trading_time = True
        else:
            self.valid_trading_time = False

        if len(self.close_ema) == 0:
            self.close_ema.append(close_value)

        if len(self.close) >= 2:
            self.change_of_close.append(self.close[-1] - self.close[-2])
            self.gain_of_close.append(self.change_of_close[-1] if self.change_of_close[-1] > 0 else 0.0)
            self.loss_of_close.append(abs(self.change_of_close[-1]) if self.change_of_close[-1] < 0 else 0.0)
        else:
            self.change_of_close.append(np.NaN)
            self.gain_of_close.append(np.NaN)
            self.loss_of_close.append(np.NaN)

        if len(self.close) >= self.period:
            self.close_sma.append(sum(self.close[-self.period:]) / self.period)
            self.close_ema.append(float(self.close[-1]) * float(2.0 / float(self.period + 1.0)) +
                                  float(self.close_ema[-1]) * float(1.0 - 2.0 / float(self.period + 1.0)))
            self.close_wma.append(sum([(self.close[-(self.period - i)] * (self.period - i)) /
                                       sum(range(self.period + 1)) for i in range(self.period)]))

        else:
            self.close_sma.append(np.NaN)
            self.close_ema.append(np.NaN)
            self.close_wma.append(np.NaN)

        # Assert that all arrays have the same amount of points in them (including defaults)
        assert (len(self.time) == len(self.open) == len(self.high) == len(self.low) == len(self.close) ==
                len(self.change_of_close) == len(self.gain_of_close) == len(self.loss_of_close))