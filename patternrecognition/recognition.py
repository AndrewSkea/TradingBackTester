import time
from enums.enums import Option
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

        self._index_of_graph_needed = -1
        self._index_of_graph = 0

    def add_to_indicators(self, close_value, low_value, high_value):
        # self._macd.add_data_point(close_value)
        # self._cci.add_to_cci_array(close_value, high_value, low_value)
        self._bband.add_to_arrays(close_value)
        # self._stoch_osc.add_to_stoch(high_value, low_value, close_value)
        self._rsi.add_point(close_value)
        self._custom_one_class.add_data_point(close_value, low_value, high_value)
        # self._awesome_oscillator_class.add_data_point(close_value, low_value, high_value)

    def recognition(self, pattern, close_value, low_value, high_value, future_close_value):
        """
        This runs the recognition process on the current pattern
        :param high_value:
        :param low_value:
        :param close_value:
        :param pattern:
        :return: null
        """
        self.add_to_indicators(close_value, low_value, high_value)
        result_array = []
        # # 0000000. This is getting the result of the percentage change indicator
        # result_array.append(Option.NO_TRADE)
        #
        # # 1111111. THis is getting the result for the MACD indicator
        # result_array.append(self._macd.get_result())
        #
        # # 2222222. This is getting the result for the CCI indicator
        # cci_result, cci_strength = self._cci.get_result()
        # result_array.append(cci_result)
        # cci_strength *= 100
        #
        # 3333333. This is getting the result for the Bollinger Bands
        result_array.append(self._bband.get_result())
        #
        # # 4444444. This is getting the result of the stochastic osc class
        # result_array.append(self._stoch_osc.get_result())

        # 5555555. Custom 1 (WMA, EMA and AO combo)
        result_array.append(self._custom_one_class.get_result())

        # 6666666. RSI
        result_array.append(self._rsi.get_result())
        #
        # # 7777777. awesome_oscillator_class
        # result_array.append(self._awesome_oscillator_class.get_result())

        indicator_1_index = 1
        indicator_2_index = 0
        indicator_3_index = 2
        if result_array[indicator_1_index] == Option.BUY and result_array[indicator_3_index] != Option.SELL:
            if close_value < future_close_value:
                self._bought_won += 1
            else:
                self._bought_failed += 1
                if self._index_of_graph == self._index_of_graph_needed:
                    self._custom_one_class.send_results_to_graph(self._graph, future_close_value,
                                                                 "BOUGHT RSI: {}".format(self._rsi.get_rsi_array()[-1]))
                self._index_of_graph += 1

        elif result_array[indicator_1_index] == Option.SELL and result_array[indicator_3_index] != Option.BUY and \
                        result_array[indicator_2_index] != Option.BUY:
            if close_value > future_close_value:
                self._sold_won += 1
            else:
                self._sold_failed += 1
                if self._index_of_graph == self._index_of_graph_needed:
                    self._custom_one_class.send_results_to_graph(self._graph, future_close_value,
                                                                 "SOLD RSI: {}".format(self._rsi.get_rsi_array()[-1]))
                self._index_of_graph += 1

        # if result_array.count(Option.BUY) >= 3:
        #     if close_value > future_close_value:
        #         self._bought_won += 1
        #         # print('CORRECT - Buy: {},  {}'.format(result_array, rsi_value))
        #     else:
        #         self._bought_failed += 1
        #         # print('FAILED - Buy: {},  {}'.format(result_array, rsi_value))
        #
        # elif result_array.count(Option.SELL) >= 3:
        #     if close_value < future_close_value:
        #         self._sold_won += 1
        #         # print('CORRECT - Sell: {},  {}'.format(result_array, rsi_value))
        #     else:
        #         self._sold_failed += 1
        #         # print('FAILED - Sell: {},  {}'.format(result_array, rsi_value))

        return tuple(result_array)

    def start(self):
        """
        This starts the pattern recognition by syncing with the server time and then
        running the recognition every minute from then on in order to trade
        :return:
        """
        num_iterations = len(self._close)
        index = 2
        self.add_to_indicators(close_value=self._close[0], low_value=self._low[0], high_value=self._high[0])
        self.add_to_indicators(close_value=self._close[1], low_value=self._low[1], high_value=self._high[1])
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

        table_data = [
            ["----", "Bought", "Sold"],
            ["Won", self._bought_won, self._sold_won],
            ["Failed", self._bought_failed, self._sold_failed]
        ]
        print("\n\nResults:\n{}".format(AsciiTable(table_data).table))
        try:
            print("   Win rate: {}%".format(100 * (self._bought_won + self._sold_won) / (
                self._bought_won + self._sold_won + self._bought_failed + self._sold_failed)))
        except:
            print("There were no results")

            # # This syncs the algorithm with the server time so it can use time.sleep later to not use any CPU
            # while self.api.get_seconds_left() != 0:
            #     # Prints the server time left
            #     sys.stdout.write('\rServer time left: {}'.format(self.api.get_seconds_left()))
            #     sys.stdout.flush()
            #     # This sleeps for 0.9 seconds seconds so that it only iterates again nearer the correct time
            #     time.sleep(0.99)
            #
            # # Adds the newest data point got from the iqoption api to the pattern for recognition
            # # try:
            # datetime, open_price, high, low, close = self.api.get_next_data_point()
            # self.add_to_indicators(close_value=close, low_value=low, high_value=high)
            # print("Before While: close: {}, high: {}, low: {}".format(close, high, low))
            # self._live_close_prices.append(close)
            # print("------------------------------------------\n")
            # # except Exception as e:
            # #     print(e)
            #
            # # Prints the length of the pattern so you know where it is up to
            # print('length of the pattern: ', len(self._live_close_prices))
            # # Sleeps so that it only runs when the minute is nearly up
            # # Create an infinite loop so that it continues trading until you manually stop it
            # while time.time():
            #     # try and catch so that it doesn't break when an error happens because it is on the server
            #     # try:
            #     #     # Gets the seconds left. If not 0 then it loops back again and tests again until it is
            #     if self.api.get_seconds_left() > 59 or self.api.get_seconds_left() <= 1:
            #         # Adds it to the current pattern so that it increases in size until length_of_pattern
            #         # print(self.api.get_next_data_point())
            #         datetime, open_price, high, low, close = self.api.get_next_data_point()
            #         print(self.recognition(None, close, low, high))
            #         self._live_close_prices.append(close)
            #         print('length of the pattern: ', len(self._live_close_prices))
            #         if len(self._live_close_prices) >= self.constants.get_pattern_len():
            #             # Run recognition on the current pattern
            #             print(self.recognition(None, close, low, high))
            #         # Sleep for nearly/  a minute to not waste CPU time
            #         time.sleep(58)
            #     # This is the exception if there are any errors, it will print them
            #     # except Exception as e:
            #     #     print('!!!!!!!!!!!!!!!!!!\nERROR\nLen: {}\nTime: {}\nError message: {}\n!!!!!!!!!!!!!!!!!!!!!'.format(
            #     #         len(self._live_close_prices), time.time(), e))

    # This is put in to avoid errors but I don't know why it is needed so leave it in
    if __name__ == '__main__':
        print('this has been called by the __main__ thing which is bad, oopsie')


        # def start(self):
        #     """
        #     This starts the pattern recognition by syncing with the server time and then
        #     running the recognition every minute from then on in order to trade
        #     :return:
        #     """
        #     result_dict = {}
        #     # Number of patterns there are
        #     max_iterations = len(self._close)
        #     index = 0
        #     while index < max_iterations - 31:
        #         # Run recognition on the current pattern
        #         result_tuple, strength_of_option = self.recognition(self.pattern_data_tuples[0][index], self._close[index],
        #                                                             self._low[index], self._high[index])
        #         if strength_of_option > self.constants.get_rsi_limit():
        #             if self.pattern_data_tuples[0][index] < self.pattern_data_tuples[0][index + 1]:
        #                 try:
        #                     temp = result_dict[result_tuple]
        #                     result_dict.update({result_tuple: (temp[0] + 1, temp[1])})
        #                 except KeyError:
        #                     result_dict.update({result_tuple: (0, 0)})
        #             elif self.pattern_data_tuples[0][index] > self.pattern_data_tuples[0][index + 1]:
        #                 try:
        #                     temp = result_dict[result_tuple]
        #                     result_dict.update({result_tuple: (temp[0], temp[1] + 1)})
        #                 except KeyError:
        #                     result_dict.update({result_tuple: (0, 0)})
        #
        #         sys.stdout.write('\r{} / {} : {}%  Close: {}'.format(index,
        #                                                              max_iterations,
        #                                                              round(float(100 * index / max_iterations), 1),
        #                                                              self._close[index]))
        #         sys.stdout.flush()
        #         index += 1
        #
        #     result_dict = sorted(result_dict.items(), key=lambda item: item[0].count(1 or 0))
        #     result_dict.reverse()
        #     self.log_and_get_percentage_win(result_dict)
        #
        #     for key, value in result_dict:
        #         if key.count(1) == 3:
        #             try:
        #                 if value[0] + value[1] > 50:
        #                     self._temp_res_array.append(float(value[0]) / float(value[0] + value[1]))
        #             except ZeroDivisionError:
        #                 pass
        #         elif key.count(1) == 2:
        #             try:
        #                 if value[0] + value[1] > 50:
        #                     self._temp_res_array.append(float(value[0]) / float(value[0] + value[1]))
        #             except ZeroDivisionError:
        #                 pass
        #         elif key.count(0) == 3:
        #             try:
        #                 if value[0] + value[1] > 50:
        #                     self._temp_res_array.append(float(value[1]) / float(value[0] + value[1]))
        #             except ZeroDivisionError:
        #                 pass
        #         elif key.count(0) == 2:
        #             try:
        #                 if value[0] + value[1] > 50:
        #                     self._temp_res_array.append(float(value[1]) / float(value[0] + value[1]))
        #             except ZeroDivisionError:
        #                 pass
        #     try:
        #         self._temp_res_array.remove(0)
        #     except:
        #         pass
        #
        #     try:
        #         avg_res = float(sum(self._temp_res_array)) / float(len(self._temp_res_array))
        #         print('Avg Result: {}\nMax Result: {} \nNum results: {}'.format(round(100 * avg_res, 1),
        #                                                                         round(100 * max(self._temp_res_array), 1),
        #                                                                         len(self._temp_res_array)))
        #         print("\n\n\r", self._temp_res_array)
        #         return avg_res
        #     except:
        #         return 0
