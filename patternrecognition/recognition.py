import time
from enums import enums
from methods.percentage_change import PercentageChange
from databases import LogHandler
from terminaltables import AsciiTable
import sys


class PatternRecognition:
    def __init__(self, pattern_array, performance_array, time_ar, open_price, high_price, low_price, close_price,
                 _patterns_array_tuple, constants_class, macd_class, cci_class, bband_class, stoch_osc, rsi_class):
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

    def recognition(self, pattern, close_value, low_value, high_value):
        """
        This runs the recognition process on the current pattern
        :param high_value:
        :param low_value:
        :param close_value:
        :param pattern:
        :return: null
        """
        result_array = []
        # This is getting the result of the percentage change indicator
        # result_array.append(self._pc.get_result_of_pc(pattern=pattern))
        result_array.append(enums.Option.NO_TRADE)

        # THis is getting the result for the MACD indicator
        self._macd.add_data_point(close_value)
        result_array.append(self._macd.get_result())

        # This is getting the result for the CCI indicator
        self._cci.add_to_cci_array(close_value, high_value, low_value)
        cci_result, cci_strength = self._cci.get_result()
        result_array.append(cci_result)
        cci_strength *= 100

        # This is getting the result for the Bollinger Bands
        self._bband.add_to_arrays(close_value)
        result_array.append(self._bband.get_result())

        # This is getting the result of the stochastic osc class
        self._stoch_osc.add_to_stoch(high_value, low_value, close_value)
        result_array.append(self._stoch_osc.get_result())

        self._rsi.add_point(close_value)
        rsi_value = self._rsi.get_result()

        index_of_array = 0
        for i in result_array:
            if i == enums.Option.BUY:
                result_array[index_of_array] = 1
            elif i == enums.Option.SELL:
                result_array[index_of_array] = 0
            else:
                result_array[index_of_array] = -1
            index_of_array += 1

        return tuple(result_array), rsi_value

    def no_patterns(self, final_time):
        """
        This is called when no patterns have been found or the criteria hasn't been  met so a standard input is
        sent to the log_handler class to insert into the database
        :param final_time: this is the time pattern recognition finished in (could be skewed if finishes early)
        :return: null
        """
        # Prints that there are no patterns and inserts the data into the db
        print('No patterns in: '.format(final_time))

    def log_and_get_percentage_win(self, result_dict):
        table_data = [['PC', 'MACD', 'CCI', 'BBAND', 'STOCH_OSC', '', '', 'Num Buys', 'Num Sells', 'Ratio']]
        for key, value in result_dict:
            if (value[0] != 0 or value[1] != 0) and key.count(-1) < 4:
                key_final = []
                for k in key:
                    if k == 0:
                        key_final.append('S')
                    elif k == 1:
                        key_final.append('B')
                    else:
                        key_final.append(' ')
                try:
                    ratio = float(value[0]) / float(value[1])
                except ZeroDivisionError:
                    if value[0] == 0:
                        ratio = value[1]
                    else:
                        ratio = value[0]

                table_data.append([key_final[0], key_final[1], key_final[2], key_final[3], key_final[4], '', '',
                                   value[0], value[1], "%.2f" % ratio])

        results_table = AsciiTable(table_data)
        print('\n', results_table.table)

        constants_class_state_table = self.constants.get_str_table()

        _file = open("logdata/log.txt", 'a')
        _file.write("\n\######################################################################################\n ")
        _file.write(constants_class_state_table)
        _file.write("\n\n\n")
        _file.write(results_table.table)
        _file.close()

    def start(self):
        """
        This starts the pattern recognition by syncing with the server time and then
        running the recognition every minute from then on in order to trade
        :return:
        """
        result_dict = {}
        # Number of patterns there are
        max_iterations = len(self._close)
        index = 0
        while index < max_iterations - 31:
            # Run recognition on the current pattern
            result_tuple, strength_of_option = self.recognition(self.pattern_data_tuples[0][index], self._close[index],
                                                                self._low[index], self._high[index])
            if strength_of_option > self.constants.get_rsi_limit():
                if self.pattern_data_tuples[0][index] < self.pattern_data_tuples[0][index + 1]:
                    try:
                        temp = result_dict[result_tuple]
                        result_dict.update({result_tuple: (temp[0] + 1, temp[1])})
                    except KeyError:
                        result_dict.update({result_tuple: (0, 0)})
                elif self.pattern_data_tuples[0][index] > self.pattern_data_tuples[0][index + 1]:
                    try:
                        temp = result_dict[result_tuple]
                        result_dict.update({result_tuple: (temp[0], temp[1] + 1)})
                    except KeyError:
                        result_dict.update({result_tuple: (0, 0)})

            sys.stdout.write('\r{} / {} : {}%  Close: {}'.format(index,
                                                                 max_iterations,
                                                                 round(float(100 * index / max_iterations), 1),
                                                                 self._close[index]))
            sys.stdout.flush()
            index += 1

        result_dict = sorted(result_dict.items(), key=lambda item: item[0].count(1 or 0))
        result_dict.reverse()
        self.log_and_get_percentage_win(result_dict)

        for key, value in result_dict:
            if key.count(1) == 3:
                try:
                    if value[0] + value[1] > 50:
                        self._temp_res_array.append(float(value[0]) / float(value[0] + value[1]))
                except ZeroDivisionError:
                    pass
            elif key.count(1) == 2:
                try:
                    if value[0] + value[1] > 50:
                        self._temp_res_array.append(float(value[0]) / float(value[0] + value[1]))
                except ZeroDivisionError:
                    pass
            elif key.count(0) == 3:
                try:
                    if value[0] + value[1] > 50:
                        self._temp_res_array.append(float(value[1]) / float(value[0] + value[1]))
                except ZeroDivisionError:
                    pass
            elif key.count(0) == 2:
                try:
                    if value[0] + value[1] > 50:
                        self._temp_res_array.append(float(value[1]) / float(value[0] + value[1]))
                except ZeroDivisionError:
                    pass
        try:
            self._temp_res_array.remove(0)
        except:
            pass

        try:
            avg_res = float(sum(self._temp_res_array)) / float(len(self._temp_res_array))
            print('Avg Result: {}\nMax Result: {} \nNum results: {}'.format(round(100 * avg_res, 1),
                                                                            round(100 * max(self._temp_res_array), 1),
                                                                            len(self._temp_res_array)))
            print("\n\n\r", self._temp_res_array)
            return avg_res
        except:
            return 0
