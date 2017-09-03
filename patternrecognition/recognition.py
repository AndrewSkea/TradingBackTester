import time
import enums
from iqoption import iqapi
from methods.percentage_change import PercentageChange
from methods.macd import MACD
from databases import LogHandler


class PatternRecognition:
    def __init__(self, _data_array_tuple, _patterns_array_tuple, _indicator_data_array_tuple, constants_class,
                 macd_class):
        """
        This initialises all the data that is needed in this class
        :param array_data_tuple: 
        """
        # Instance for the constants class
        self.constants = constants_class
        # Tuple for all the past data
        array_data_tuple = _data_array_tuple
        # Tuple for the live patterns
        self.pattern_data_tuples = _patterns_array_tuple
        # This is the array that has the historic data patterns that end up buying
        self._pattern_array = array_data_tuple[0]
        # This is the buy performance array which is the pattern's outcome (same index as pattern)
        self._performance_array = array_data_tuple[1]
        # This is the array that has the historic data patterns that end up selling
        self._time = array_data_tuple[2]
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._high = array_data_tuple[3]
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._low = array_data_tuple[4]
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._close = array_data_tuple[5]
        # Instance of Log handler
        self._log_handler = LogHandler()
        # Number of bets
        self._num_bets = 0
        # MACD class instance
        self._macd = macd_class
        # Percentage Change class
        self._pc = PercentageChange(self.constants, self._pattern_array, self._performance_array)

    def recognition(self, pattern, close_value):
        """
        This runs the recognition process on the current pattern
        :param pattern:
        :return: null
        """
        strength_of_option = 0
        option = enums.Option.NO_TRADE

        percentage_change_result = self._pc.get_result_of_pc(pattern=pattern)
        self._macd.add_data_point(close_value)
        macd_result = self._macd.get_result()

        if macd_result == enums.Direction.UP:
            if percentage_change_result == enums.Option.BUY:
                option = enums.Option.BUY
                strength_of_option = 10
            elif percentage_change_result == enums.Option.SELL:
                option = enums.Option.SELL
                strength_of_option = 3
            else:
                option = enums.Option.BUY
                strength_of_option = 2
        elif macd_result == enums.Direction.DOWN:
            if percentage_change_result == enums.Option.BUY:
                option = enums.Option.BUY
                strength_of_option = 3
            elif percentage_change_result == enums.Option.SELL:
                option = enums.Option.SELL
                strength_of_option = 10
            else:
                option = enums.Option.SELL
                strength_of_option = 2
        else:
            # No patterns have been found or criteria not met
            if percentage_change_result == enums.Option.BUY:
                option = enums.Option.BUY
                strength_of_option = 1
            elif percentage_change_result == enums.Option.SELL:
                option = enums.Option.SELL
                strength_of_option = 1
            else:
                option = enums.Option.NO_TRADE
                strength_of_option = 0

        return option, strength_of_option

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
        # Number of patterns there are
        max_iterations = len(self.pattern_data_tuples[0])
        print 'Number of iterations: ', max_iterations
        _num_no_trades = 0
        index = 0
        while index < max_iterations - 1:
            # Run recognition on the current pattern
            option, strength_of_option = self.recognition(self.pattern_data_tuples[0][index], self._close[index])
            if option == enums.Option.NO_TRADE:
                _num_no_trades += 1
                print index, " - No Trades"
            else:
                if self.pattern_data_tuples[0][index] < self.pattern_data_tuples[0][index + 1]:
                    if option == enums.Option.BUY:
                        result_array.append((1, strength_of_option))
                        print index, ' - WIN x ', strength_of_option
                    elif option == enums.Option.SELL:
                        result_array.append((-1, strength_of_option))
                        print index, ' - LOSE x ', strength_of_option
                elif self.pattern_data_tuples[0][index] > self.pattern_data_tuples[0][index + 1]:
                    if option == enums.Option.BUY:
                        result_array.append((-1, strength_of_option))
                        print index, ' - LOSE x ', strength_of_option
                    elif option == enums.Option.SELL:
                        result_array.append((1, strength_of_option))
                        print index, ' - WIN x ', strength_of_option
                else:
                    result_array.append((0, strength_of_option))
                    print index, ' - DRAW x ', strength_of_option
            index += 1

        _num_wins_strength_1 = result_array.count((1, 1))
        _num_wins_strength_2 = result_array.count((1, 2))
        _num_wins_strength_3 = result_array.count((1, 3))
        _num_wins_strength_10 = result_array.count((1, 10))
        _num_loses_strength_1 = result_array.count((-1, 1))
        _num_loses_strength_2 = result_array.count((-1, 2))
        _num_loses_strength_3 = result_array.count((-1, 3))
        _num_loses_strength_10 = result_array.count((-1, 10))
        _num_draws_strength_0 = result_array.count((0, 0))

        _num_wins = _num_wins_strength_1 + _num_wins_strength_2 + _num_wins_strength_3 + _num_wins_strength_10
        _num_loses = _num_loses_strength_1 + _num_loses_strength_2 + _num_loses_strength_3 + _num_loses_strength_10
        _num_draws = _num_draws_strength_0
        _total_num_iterations = _num_wins + _num_loses + _num_draws + _num_no_trades
        _rest_of_iterations = max_iterations - _total_num_iterations

        _percentage_win = float(_num_wins) / float(_num_loses + _num_draws + _num_wins)

        print '\n\n\n\nPercentage win = ', _percentage_win, '\n', \
            '_num_wins_strength_1  = ', _num_wins_strength_1, '\n', \
            '_num_wins_strength_2  = ', _num_wins_strength_2, '\n', \
            '_num_wins_strength_3  = ', _num_wins_strength_3, '\n', \
            '_num_wins_strength_10 = ', _num_wins_strength_10, '\n', \
            '_num_loses_strength_1 = ', _num_loses_strength_1, '\n', \
            '_num_loses_strength_2 = ', _num_loses_strength_2, '\n', \
            '_num_loses_strength_3 = ', _num_loses_strength_3, '\n', \
            '_num_loses_strength_10 = ', _num_loses_strength_10, '\n', \
            '_num_draws_strength_0 = ', _num_draws_strength_0, '\n', \
            '_num_no_trades = ', _num_no_trades, '\n', \
            '_total_num_iterations = ', _total_num_iterations

        result_csv_string = ',{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
            _percentage_win,
            _num_wins_strength_1,
            _num_wins_strength_2,
            _num_wins_strength_3,
            _num_wins_strength_10,
            _num_loses_strength_1,
            _num_loses_strength_2,
            _num_loses_strength_3,
            _num_loses_strength_10,
            _num_draws_strength_0,
            _num_no_trades,
            _total_num_iterations,
            _rest_of_iterations)

        log_string = self.constants.get_csv_str() + result_csv_string

        f = open("logdata/log.csv", 'a')
        f.write(log_string)
        f.close()
        return _percentage_win

    # This is put in to avoid errors but I don't know why it is needed so leave it in
    if __name__ == '__main__':
        print 'this has been called by the __main__ thing which is bad'
