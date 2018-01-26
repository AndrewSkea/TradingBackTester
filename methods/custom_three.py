from enums.enums import Option
from methods import ema, sma


class CustomThree:
    def __init__(self, constants):
        self._close_prices = []
        self._high_prices = []
        self._low_prices = []
        self.constants = constants

        self._ema_a = ema.EMA(13)

        self._ema_b = ema.EMA(1)
        self._ema_c = ema.EMA(1)
        self._ema_d = ema.EMA(1)

        self._ema_e = ema.EMA(8)
        self._ema_f = ema.EMA(5)

        self._ema_slow = ema.EMA(8)
        self._ema_fast = ema.EMA(5)

        self._sma_a = sma.SMA(8)
        self._sma_b = sma.SMA(13)

        self._bearish = False
        self._bullish = False

        self._highest_of_last_period = 0
        self._lowest_of_last_period = 0

        self._trend_up_array = []
        self._trend_down_array = []
        self._down_array = []
        self._up_array = []
        self._trend = []

        self._RSTT = []
        self._RSTB = []
        self._RST = 21

        self._result_array = []

    def just_add_data(self, close_value, low_value, high_value):
        self._close_prices.append(close_value)
        self._high_prices.append(high_value)
        self._low_prices.append(low_value)
        print("HI")

    def add_data_point(self, close_value, low_value, high_value):
        self._close_prices.append(close_value)
        self._high_prices.append(high_value)
        self._low_prices.append(low_value)

        self._sma_a.add_data_point(close_value)
        self._highest_of_last_period = max(self._close_prices[-13:])
        self._lowest_of_last_period = min(self._close_prices[-13:])

        self._bearish = True if self._close_prices[-1] > self._sma_a.get_sma_array()[-1] else False
        self._bullish = True if self._close_prices[-1] < self._sma_a.get_sma_array()[-1] else False

        self._ema_a.add_data_point(close_value)

        ema_fast = self._ema_fast.add_data_point(max((low_value + close_value) / 2, 5))
        ema_slow = self._ema_slow.add_data_point(min((high_value + close_value) / 2, 8))

        ema_b = self._ema_b.add_data_point(close_value)
        ema_c = self._ema_c.add_data_point(ema_b)
        ema_d = self._ema_d.add_data_point(ema_c)
        tema = 1 * (ema_b - ema_c) + ema_d

        ema_e = self._ema_e.add_data_point(close_value)
        ema_f = self._ema_f.add_data_point(ema_e)
        dema = 2 * ema_e - ema_f

        # signal = max(ema_fast, ema_slow) if tema > dema else min(ema_fast, ema_slow)
        # is_call = tema > dema and signal > low_value and (signal - signal[1] > signal[1] - signal[2])
        # is_put = tema < dema and signal < high_value and (signal[1] - signal > signal[2] - signal[1])

        self._up_array.append((high_value + low_value) / 2 - (1 * self.average_true_range()))
        self._down_array.append((high_value + low_value) / 2 + (1 * self.average_true_range()))

        if len(self._trend_up_array) <= 2:
            self._trend_up_array.append(self._up_array[-1])
        else:
            self._trend_up_array.append(
                max(self._up_array[-1], self._trend_up_array[-1]) if self._close_prices[-2] > self._trend_up_array[
                    -2] else
                self._up_array[-1])
        if len(self._trend_down_array) <= 2:
            self._trend_down_array.append(self._down_array[-1])
        else:
            self._trend_down_array.append(
                min(self._down_array[-1], self._trend_down_array[-1]) if self._close_prices[-2] <
                                                                         self._trend_down_array[-2]
                else self._down_array[-1])

        if len(self._trend_down_array) > 2:
            temp = 0
            if self._close_prices[-1] > self._trend_down_array[-2]:
                temp = 1
            else:
                if self._close_prices[-1] < self._trend_up_array[-2]:
                    temp = -1
                else:
                    if self._trend[-1] is None:
                        temp = 0
                    else:
                        temp = self._trend[-1]
            self._trend.append(temp)

            # self._RSTT.append(self.get_last_highest_value(self._RST))
            # self._RSTB.append(self.get_last_lowest_value(self._RST))
            if len(self._trend) > 2:
                if self._trend[-1] == 1 and self._trend[-2] == -1:
                    self._result_array.append(Option.BUY)
                elif self._trend[-1] == -1 and self._trend[-2] == 1:
                    self._result_array.append(Option.SELL)
                else:
                    self._result_array.append(Option.NO_TRADE)
            else:
                self._result_array.append(Option.NO_TRADE)
        else:
            self._result_array.append(Option.NO_TRADE)

    def get_last_highest_value(self, bars_back):
        for i in range(bars_back):
            if self._high_prices[-1] >= self._high_prices[-i]:
                return self._high_prices[-i]
        return self._high_prices[-bars_back]

    def get_last_lowest_value(self, bars_back):
        for i in range(bars_back):
            if self._low_prices[-1] <= self._low_prices[-i]:
                return self._low_prices[-i]
        return self._low_prices[-bars_back]

    def average_true_range(self):
        return max((self._high_prices[-1] - self._low_prices[-1]),
                   abs(self._high_prices[-1] - self._close_prices[-2]),
                   abs(self._low_prices[-1] - self._close_prices[-2]))

    def get_result(self):
        return self._result_array[-1]
