from enums.enums import Option
import time


class RSI:
    def __init__(self, close_prices, constant_class):
        self._close_prices = list(close_prices)
        self._constants = constant_class
        self._period = self._constants.get_rsi_period()
        self._loss = []
        self._gain = []
        self._avg_gain = []
        self._avg_loss = []
        self._rs = []
        self._rsi = []

    def calculate_avg_difference(self, prev_avg, avg):
        return (prev_avg * (self._period - 1) + avg) / self._period

    def add_point(self, close_point):
        self._close_prices.append(close_point)
        if len(self._close_prices) > 2:
            diff = self._close_prices[-1] - self._close_prices[-2]
            if diff > 0:
                self._gain.append(abs(diff))
                self._loss.append(0.0)
            else:
                self._gain.append(0.0)
                self._loss.append(abs(diff))

            if len(self._close_prices) > self._period:
                self._avg_gain.append(sum(self._gain[-self._period:]) / self._period)
                self._avg_loss.append(sum(self._loss[-self._period:]) / self._period)
                self._rs.append(self._avg_gain[-1] / self._avg_loss[-1])
                self._rsi.append(100 - (100 / (1 + self._rs[-1])))

    def get_rsi_array(self):
        return self._rsi

    def get_result(self):
        """
        Returns the last value in the RSI array
        :return:
        """
        try:
            val = self._rsi[-1]
            if val > 80:
                return Option.SELL
            elif 60 <= val <= 80:
                return Option.BUY
            elif 20 <= val <= 40:
                return Option.SELL
            elif val < 20:
                return Option.BUY
            else:
                return Option.NO_TRADE
        except IndexError:
            return Option.NO_TRADE
