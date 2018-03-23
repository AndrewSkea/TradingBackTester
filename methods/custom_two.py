from enums.enums import Option
from indicators import sma
from methods import ema


class CustomTwo:
    def __init__(self, constants):
        self._close_prices = []
        self._high_prices = []
        self._low_prices = []
        self._crossover_array = []
        self._overbought_level_1 = 60
        self._overbought_level_2 = 53
        self._oversold_level_2 = -53
        self._oversold_level_1 = -60
        self.constants = constants
        self._ema_a = ema.EMA(10)
        self._ema_b = ema.EMA(21)
        self._ema_c = ema.EMA(10)
        self._sma_a = sma.SMA(4)

    def add_data_point(self, close_value, low_value, high_value):
        self._close_prices.append(close_value)
        self._high_prices.append(high_value)
        self._low_prices.append(low_value)

        hlc3 = float(close_value + high_value + low_value) / 3.0

        ema_a_result = self._ema_a.add_data_point(hlc3)
        ema_c_result = self._ema_c.add_data_point(abs(hlc3 - self._ema_a.get_last_point_ema_array()))
        try:
            ci = (hlc3 - float(ema_a_result)) / (0.015 * ema_c_result)
            tci = self._ema_b.add_data_point(ci)
            self._sma_a.add_data_point(tci)
        except ZeroDivisionError:
            pass

    def send_results_to_graph(self, graph1, future_close_point, title_text):
        overbought_array = []
        oversold_array = []
        for i in range(200):
            overbought_array.append(self._overbought_level_1)
            oversold_array.append(self._oversold_level_1)
        graph1.start(overbought_array, self._ema_b.get_ema_array(), self._ema_c.get_ema_array(),
                     self._sma_a.get_sma_array(), oversold_array, future_close_point, title_text)

    def get_result(self):
        sma_arr = self._sma_a.get_sma_array()
        ema_arr = self._ema_b.get_ema_array()
        try:
            sma_option = Option.NO_TRADE
            ema_option = Option.NO_TRADE
            if (ema_arr[-2] < self._overbought_level_2 < ema_arr[-3] and (
                                ema_arr[-4] > self._overbought_level_1 or
                                ema_arr[-5] > self._overbought_level_1 or
                                ema_arr[-6] > self._overbought_level_1)):
                ema_option = Option.SELL
            elif (ema_arr[-2] > self._oversold_level_2 > ema_arr[-3] and (
                                ema_arr[-4] < self._oversold_level_1 or
                                ema_arr[-5] < self._oversold_level_1 or
                                ema_arr[-6] < self._oversold_level_1)):
                ema_option = Option.BUY

            if (sma_arr[-1] < self._overbought_level_2 < sma_arr[-2] and (
                                sma_arr[-2] > self._overbought_level_1 or
                                sma_arr[-3] > self._overbought_level_1 or
                                sma_arr[-4] > self._overbought_level_1)):
                sma_option = Option.SELL
            elif (sma_arr[-1] > self._oversold_level_2 > sma_arr[-2] and (
                                sma_arr[-2] < self._oversold_level_1 or
                                sma_arr[-3] < self._oversold_level_1 or
                                sma_arr[-4] < self._oversold_level_1)):
                sma_option = Option.BUY

            if ema_option == sma_option:
                return ema_option
        except IndexError:
            return Option.NO_TRADE
