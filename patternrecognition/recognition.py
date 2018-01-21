import time
from enums.enums import Option, Indicators
from methods.percentage_change import PercentageChange
from databases import LogHandler
from terminaltables import AsciiTable
# from iqoption import IQOptionApi
from graph.graph import LiveGraph
import sys


class PatternRecognition:
    def __init__(self, pattern_array, performance_array, time_ar, open_price, high_price, low_price, close_price,
                 _patterns_array_tuple, constants_class, macd_class, cci_class, bband_class, stoch_osc, rsi_class,
                 custom_one_class, awesome_oscillator_class):
        """
        :param pattern_array:
        :param performance_array:
        :param time_ar:
        :param open_price:
        :param high_price:
        :param low_price:
        :param close_price:
        :param _patterns_array_tuple:
        :param constants_class:
        :param macd_class:
        :param cci_class:
        :param bband_class:
        :param stoch_osc:
        :param rsi_class:
        """
        # Creates an instance of the iq options api class of this project
        # self.api = IQOptionApi()
        # Instance for the constants class
        self.constants = constants_class
        # Tuple for the live patterns
        self.pattern_data_tuples = _patterns_array_tuple
        # This is the array that has the historic data patterns that end up buying
        self._pattern_array = pattern_array
        # This is the buy performance array which is the pattern's outcome (same index as pattern)
        self._performance_array = performance_array
        # This is the array that has the historic data patterns that end up selling
        self._time = time_ar
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._high = high_price
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._low = low_price
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._close = close_price
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._open = open_price
        # Instance of Log handler
        self._log_handler = LogHandler()
        # Number of bets
        self._num_bets = 0
        # MACD class instance
        self._macd = macd_class
        # Percentage Change class
        self._pc = PercentageChange(self.constants, self._pattern_array, self._performance_array)
        # CCI Class
        self._cci = cci_class
        # BBand class Class
        self._bband = bband_class
        # THis is the Stochastic Oscillator classs
        self._stoch_osc = stoch_osc
        # Result array
        self._temp_res_array = []
        # This is the RSI Class
        self._rsi = rsi_class
        # This is the live close prices to get length of how many times we have got data
        self._live_close_prices = []
        # This is the Cusstom ONE CLASS
        self._custom_one_class = custom_one_class
        self._awesome_oscillator_class = awesome_oscillator_class
        self._graph = LiveGraph()
        self._bought_failed = 0
        self._bought_won = 0
        self._sold_failed = 0
        self._sold_won = 0
        self._index_of_graph_needed = -5
        self._index_of_graph = 0

    def send_results_to_graph(self, future_close_val, title):
        if self._index_of_graph == self._index_of_graph_needed:
            self._bband.send_results_to_graph(self._graph, future_close_val, title)
        self._index_of_graph += 1

    def add_to_indicators(self, close_value, low_value, high_value):
        self._macd.add_data_point(close_value)
        self._cci.add_to_cci_array(close_value, high_value, low_value)
        self._bband.add_to_arrays(close_value)
        self._stoch_osc.add_to_stoch(high_value, low_value, close_value)
        self._rsi.add_point(close_value)
        self._custom_one_class.add_data_point(close_value, low_value, high_value)
        self._awesome_oscillator_class.add_data_point(low_value, high_value)

    def recognition(self, pattern, close_value, low_value, high_value, future_close_value):
        """
        This runs the recognition process on the current pattern
        :param future_close_value:
        :param high_value:
        :param low_value:
        :param close_value:
        :param pattern:
        :return: null
        """
        self.add_to_indicators(close_value, low_value, high_value)
        result_dict = {
            Indicators.RSI:         self._rsi.get_result(),
            Indicators.MACD:        self._macd.get_result(),
            Indicators.CCI:         self._cci.get_result(),
            Indicators.BBAND:       self._bband.get_result(),
            Indicators.STOCHOSC:    self._stoch_osc.get_result(),
            Indicators.CUST_1:      self._custom_one_class.get_result(),
            Indicators.AO:          self._awesome_oscillator_class.get_result()
        }

        indicator_1_val = result_dict[Indicators.CUST_1]
        indicator_2_val = result_dict[Indicators.CUST_1]

        if indicator_1_val == Option.BUY and indicator_2_val == Option.BUY:
            if close_value < future_close_value:
                self._bought_won += 1
            else:
                self._bought_failed += 1
                self.send_results_to_graph(future_close_value, "BOUGHT FAILED")

        elif indicator_1_val == Option.SELL and indicator_2_val == Option.SELL:
            if close_value > future_close_value:
                self._sold_won += 1
            else:
                self._sold_failed += 1
                self.send_results_to_graph(future_close_value, "SOLD FAILED")

    def start(self):
        """
        This starts the pattern recognition by syncing with the server time and then
        running the recognition every minute from then on in order to trade
        :return:
        """
        num_iterations = len(self._close)
        index = 3
        self.add_to_indicators(close_value=self._close[0], low_value=self._low[0], high_value=self._high[0])
        self.add_to_indicators(close_value=self._close[1], low_value=self._low[1], high_value=self._high[1])
        self.add_to_indicators(close_value=self._close[2], low_value=self._low[2], high_value=self._high[2])
        while index + 3 < num_iterations:
            self._live_close_prices.append(self._close[index])
            self.recognition(None,
                             close_value=self._close[index],
                             low_value=self._low[index],
                             high_value=self._high[index],
                             future_close_value=self._close[index + 1])

            sys.stdout.write('\r{}/{}'.format(index, num_iterations))
            sys.stdout.flush()
            index += 1

        total = self._bought_won + self._sold_won + self._bought_failed + self._sold_failed
        num_won = self._bought_won + self._sold_won
        perc_win = (100 * num_won / total) if total != 0 else 0

        print("\n\n{}".format(AsciiTable([
            ["Result", "Bought", "Sold", "/\/\\", "Stat", "Value"],
            ["Won", self._bought_won, self._sold_won, "/\/\\", "Win Rate", "{} %".format(perc_win)],
            ["Failed", self._bought_failed, self._sold_failed, "/\/\\", "Num Trades", total]]).table))

