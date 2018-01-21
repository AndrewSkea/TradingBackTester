from enums.enums import Position, Trend, Option
from methods import ema, wma, awesome_oscillator, sma
from graph.graph import LiveGraph
import time


class CustomOne:
    def __init__(self, constants):
        self._all_data = []
        self.constants = constants
        self._ema_a = ema.EMA(25)
        self._ema_b = ema.EMA(18)
        self._sma_a = sma.SMA(3)
        self._wma = wma.WMA(7)
        self._awesome_oscillator = awesome_oscillator.AwesomeOscillator(self.constants)
        self._last_status = Position.EQUAL
        self._result_array = []
        self._awe_osc_result_array = []

    def add_data_point(self, close_value, low_value, high_value):
        try:
            self._all_data.append(close_value)
            self._sma_a.add_data_point(close_value)
            ema_a_last_value = self._ema_a.add_data_point(close_value)
            ema_b_last_value = self._ema_b.add_data_point(close_value)
            wma_last_value = self._wma.add_data_point(close_value)
            self._awesome_oscillator.add_data_point(low_value, high_value)

            if wma_last_value > ema_a_last_value and wma_last_value > ema_b_last_value:
                self._result_array.append(Position.ABOVE)
            elif wma_last_value < ema_a_last_value and wma_last_value < ema_b_last_value:
                self._result_array.append(Position.BELOW)
            else:
                self._result_array.append(Position.EQUAL)
        except TypeError:
            pass

    def send_results_to_graph(self, graph1, future_close_point, title_text):
        graph1.start(self._ema_a.get_ema_array(), self._ema_b.get_ema_array(), self._wma.get_wma_array(),
                     self._sma_a.get_sma_array(), self._all_data, future_close_point, title_text)

    def get_result(self):
        """
        This function returns a value if there has been a crossover
        :return: None if no crossover, else direction of crossover
        """
        sma_array = self._sma_a.get_sma_array()
        self._awe_osc_result_array.append(self._awesome_oscillator.get_result())
        try:
            custom1_result = Position.EQUAL
            if self._result_array[-1] == Position.ABOVE and self._result_array[-2] != Position.ABOVE or \
                    (self._result_array[-1] == Position.ABOVE and self._result_array[-2] == Position.ABOVE
                     and self._result_array[-3] == Position.BELOW):
                custom1_result = Option.BUY
            elif self._result_array[-1] == Position.BELOW and self._result_array[-2] != Position.BELOW or \
                    (self._result_array[-1] == Position.BELOW and self._result_array[-2] == Position.BELOW
                     and self._result_array[-3] == Position.ABOVE):
                custom1_result = Option.SELL

            if custom1_result == Option.BUY and self._awe_osc_result_array[-1] == Option.BUY:
                return Option.BUY
            elif custom1_result == Option.SELL and self._awe_osc_result_array[-1] == Option.SELL:
                return Option.SELL
            return Option.NO_TRADE

        except IndexError:
            return Option.NO_TRADE
