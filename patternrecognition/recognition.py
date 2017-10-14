import time
import enums
from methods.percentage_change import PercentageChange
from databases import LogHandler
from terminaltables import AsciiTable


class PatternRecognition:
    def __init__(self, pattern_array, performance_array, time_ar, open_price, high_price, low_price, close_price, _patterns_array_tuple, constants_class,
                 macd_class, cci_class, bband_class):
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
        #result_array.append(enums.Option.NO_TRADE)

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

        index_of_array = 0
        for i in result_array:
            if i == enums.Option.BUY:
                result_array[index_of_array] = 1
            elif i == enums.Option.SELL:
                result_array[index_of_array] = 0
            else:
                result_array[index_of_array] = -1
            index_of_array += 1

        return tuple(result_array), cci_strength

        #  if r == (0, 0, 0):
        #     return enums.Option.SELL, cci_strength + 20
        # elif r ==
        # elif r == (1, 1, 1):
        #     return enums.Option.BUY, cci_strength + 20
        #
        # if r == (0, 0, 0):
        #     return enums.Option.BUY, cci_strength + 1
        # elif r == (0, 0, 1):
        #     return enums.Option.BUY, cci_strength + 2
        # elif r == (0, 1, 0):
        #     return enums.Option.BUY, cci_strength + 3
        # elif r == (0, 1, 1):
        #     return enums.Option.BUY, cci_strength + 4
        # elif r == (1, 0, 0):
        #     return enums.Option.BUY, cci_strength + 5
        # elif r == (1, 0, 1):
        #     return enums.Option.BUY, cci_strength + 6
        # elif r == (1, 1, 0):
        #     return enums.Option.BUY, cci_strength + 7
        # elif r == (-1, 1, 1):
        #     return enums.Option.BUY, cci_strength + 8
        # elif r == (1, 1, 1):
        #     return enums.Option.BUY, cci_strength + 9
        # else:
        #     return enums.Option.NO_TRADE, 0

    def no_patterns(self, final_time):
        """
        This is called when no patterns have been found or the criteria hasn't been  met so a standard input is
        sent to the log_handler class to insert into the database
        :param final_time: this is the time pattern recognition finished in (could be skewed if finishes early)
        :return: null
        """
        # Prints that there are no patterns and inserts the data into the db
        print 'No patterns in: '.format(final_time)

    def start(self):
        """
        This starts the pattern recognition by syncing with the server time and then
        running the recognition every minute from then on in order to trade
        :return:
        """
        result_array = []
        result_dict = {}
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                for k in range(-1, 2, 1):
                    result_array.append((i, j, k))

        result_dict = {result_array[i]: [0, 0, 0] for i in range(len(result_array))}

        # Number of patterns there are
        max_iterations = len(self.pattern_data_tuples[0])
        print 'Number of iterations: ', max_iterations
        index = 0
        while index < max_iterations - 1:
            # Run recognition on the current pattern
            _start_time = time.time()
            result_tuple, strength_of_option = self.recognition(self.pattern_data_tuples[0][index], self._close[index],
                                                          self._low[index], self._high[index])
            _end_time = time.time() - _start_time
            if self.pattern_data_tuples[0][index] < self.pattern_data_tuples[0][index + 1]:
                result_dict[result_tuple][0] += 1
                # print index, ' - BUY x ', strength_of_option, 'in ', _end_time
            elif self.pattern_data_tuples[0][index] > self.pattern_data_tuples[0][index + 1]:
                result_dict[result_tuple][1] += 1
                # print index, ' - SELL x ', strength_of_option, 'in ', _end_time
            elif self.pattern_data_tuples[0][index] == self.pattern_data_tuples[0][index + 1]:
                result_dict[result_tuple][2] += 1
                # print index, ' - DRAW x ', strength_of_option, 'in ', _end_time
            else:
                # print index, ' - NO TRADE x ', strength_of_option, 'in ', _end_time
                pass
            index += 1

        return self.log_and_get_percentage_win(result_dict, max_iterations)

    def log_and_get_percentage_win(self, result_dict, max_iterations):

        print 'Number of iterations: ', max_iterations
        table_data = [['Tuple', 'Bought', 'Sold']]
        for key, value in result_dict.iteritems():
            table_data.append([str(key), str(value[0]), str(value[1])])

        table = AsciiTable(table_data)
        print table.table

    # This is put in to avoid errors but I don't know why it is needed so leave it in
    if __name__ == '__main__':
        print 'this has been called by the __main__ thing which is bad, this is needed for go knows what reason'
