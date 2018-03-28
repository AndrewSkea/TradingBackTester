import time
from methods import custom_four as C4
import tensorflow as tf
from terminaltables import AsciiTable
import sys
from enums.enums import Option, Indicators
from graph.graph import LiveGraph
from constants import finalconstants as const


# https://blog.altoros.com/tensorflow-for-foreign-exchange-market-analyzing-time-series-data.html

class PatternRecognition:
    def __init__(self, data_array_class, time_ar, open_price, high_price, low_price, close_price):

        self.data = data_array_class
        self._time = time_ar
        self._high = high_price
        self._low = low_price
        self._close = close_price
        self._open = open_price

        self.method = C4.CustomFour(self.data)

        self._graph = LiveGraph()
        self._bought_failed = 0
        self._bought_won = 0
        self._sold_failed = 0
        self._sold_won = 0
        self._index_of_graph_needed = -10
        self._index_of_graph = 0

        self._n_nodes_hl1 = 500
        self._n_nodes_hl2 = 500
        self._n_nodes_hl3 = 500

        self._n_classes = 10
        self._batch_size = 100

        self._x = tf.placeholder('float', [None, ])
        self._y = tf.placeholder('float')

    def recognition(self, index, time_value, close_value, open_value, low_value, high_value, future_close_value):
        self.data.add_data(time_value=time_value, open_value=open_value,
                           close_value=close_value, low_value=low_value, high_value=high_value)
        self.method.update_data_arrays()

        if self.data.valid_trading_time:
            if self.method.get_result() == Option.BUY:
                if close_value < future_close_value:
                    self._bought_won += 1
                    # print("Index: {}\tOpen: {:.5f}\tHigh: {:.5f}\tLow: {:.5f}\tClose: {:.5f}\tTime:{}\tBought and Won".format(index, open_value, high_value, low_value, close_value, time_value))
                elif close_value > future_close_value:
                    self._bought_failed += 1
                    # print("Index: {}\tOpen: {:.5f}\tHigh: {:.5f}\tLow: {:.5f}\tClose: {:.5f}\tTime:{}\tBought and Failed".format(index, open_value, high_value, low_value, close_value, time_value))
            elif self.method.get_result() == Option.SELL:
                if close_value > future_close_value:
                    self._sold_won += 1
                    # print("Index: {}\tOpen: {:.5f}\tHigh: {:.5f}\tLow: {:.5f}\tClose: {:.5f}\tTime:{}\tSold and Won".format(index, open_value, high_value, low_value, close_value, time_value))
                elif close_value < future_close_value:
                    self._sold_failed += 1
                    # print("Index: {}\tOpen: {:.5f}\tHigh: {:.5f}\tLow: {:.5f}\tClose: {:.5f}\tTime:{}\tSold and Failed".format(index, open_value, high_value, low_value, close_value, time_value))

    def create_nn_csv(self, close_value, low_value, high_value, future_close_value):
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
            Indicators.RSI: self._rsi.get_rsi_result_for_nn(),
            Indicators.MACD: self._macd.get_result_for_nn(),
            Indicators.CCI: self._cci.get_cci_result_for_nn(),
            Indicators.BBAND: self._bband.get_result_for_nn(),
            Indicators.STOCHOSC: self._stoch_osc.get_stoch_osc_result_for_nn(),
            Indicators.AO: self._awesome_oscillator_class.get_awesome_oscillator_result_for_nn(),
        }

        ffile_obj = open('results_2.csv', 'a')
        file_string = "\n"
        for ind_key, ind_value in result_dict.items():
            if ind_value is None:
                print(ind_key)
            file_string += str(ind_value) + ','

        if close_value < future_close_value:
            file_string += "BUY"
        elif close_value > future_close_value:
            file_string += "SELL"
        else:
            file_string += "NO_TRADE"

        ffile_obj.write(file_string)
        ffile_obj.close()

    def start(self):
        """
        This starts the pattern recognition by syncing with the server time and then
        running the recognition every minute from then on in order to trade
        :return:
        """
        with open('logdata/cci_test.txt', 'a') as log_file:
            log_file.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format("CCI Lower", "CCI Upper", "CCI Period",
                                                                           "Bought Won", "Bought Failed",
                                                                           "Sold Won", "Sold Failed",
                                                                           "Total Won", "Total Lost",
                                                                           "Bought %", "Sold %", "Total %", "Total £"))
        # total_iteration = 0
        # max_money = 0
        # for period in range(14, 22, 1):
        #     for upper in range(140, 240, 10):
        #         for lower in range(130, 200, 10):
        #             self._bought_won = 0
        # self._sold_won = 0
        # self._bought_failed = 0
        # self._sold_failed = 0
        # const.cci_upper_limit = upper
        # const.cci_lower_limit = lower
        # const.cci_period = period
        # self.method = C4.CustomFour(self.data)
        # total_iteration += 1
        start_time = time.time()
        num_iterations = len(self._close)
        for index in range(num_iterations - 1):
            self.recognition(index,
                             time_value=self._time[index],
                             close_value=self._close[index],
                             open_value=self._open[index],
                             low_value=self._low[index],
                             high_value=self._high[index],
                             future_close_value=self._close[index + 1])
            # sys.stdout.write('\r{}/{}'.format(index, num_iterations))
            # sys.stdout.flush()

        total = self._bought_won + self._sold_won + self._bought_failed + self._sold_failed
        num_won = self._bought_won + self._sold_won
        num_lost = self._bought_failed + self._sold_failed
        per_win = int((100 * num_won / total) if total != 0 else 0)
        bought_per_win = int(100 * self._bought_won / (self._bought_won + self._bought_failed))
        sold_per_win = int(100 * self._sold_won / (self._sold_failed + self._sold_won))

        final_money = (100 * 0.8 * num_won) - (100 * num_lost)
        final__money_string = "£{}".format(final_money)

        with open('logdata/log.txt', 'a') as log_file:
            log_str = "\nAfter {}s, {} trades and a net profit of {}:\n{}" \
                .format(int(time.time() - start_time), total, final__money_string,
                        AsciiTable([
                            ["Result", "Bought", "Sold", "Total"],
                            ["Won", self._bought_won, self._sold_won, num_won],
                            ["Failed", self._bought_failed, self._sold_failed, total - num_won],
                            ["Totals", str(bought_per_win) + "%", str(sold_per_win) + "%",
                             str(per_win) + "%"]]).table)

            print(log_str)
            log_file.write(
                "{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(const.cci_lower_limit,
                                                                const.cci_upper_limit,
                                                                const.cci_period,
                                                                self._bought_won, self._bought_failed,
                                                                self._sold_won, self._sold_failed,
                                                                total, num_won, num_lost,
                                                                bought_per_win, sold_per_win, per_win,
                                                                final_money))

                    # if final_money > max_money:
                    #     max_money = final_money
                    #     print(max_money)
