import time
import enums
from iqoption import iqapi
from methods import percentage_change
from databases import LogHandler


class PatternRecognition:
    def __init__(self, _data_array_tuple, _patterns_array_tuple, constants_class):
        """
        This initialises all the data that is needed in this class
        :param array_data_tuple: 
        """
        self.constants = constants_class
        array_data_tuple = _data_array_tuple
        self.pattern_data_tuples = _patterns_array_tuple
        # Creates an instance of the iq options api class of this project
        self.api = iqapi.IQOptionApi()
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

    def analyse_pattern(self, pattern):
        """
        This function goes through all the data in the arrays and returns the amount of similar patterns
        :return: returns the predicted outcomes array which holds all the outcomes from the similar patterns
        """
        # This is the array of predicted outcomes from all the patterns
        _predicted_outcomes_array = []
        # iterates through the historic data array to find similar patterns
        for b in range(len(self._pattern_array)):
            # Uses a should skip boolean to check whether to skip the current pattern completely
            _should_skip = False
            # Gets the pattern that it will use
            _each_pattern = self._pattern_array[b]
            # Goes through the pattern and sees if each percentage change is within the right limit, else continue
            for i in range(0, self.constants.get_pattern_len() - 1, 1):
                if abs(percentage_change.percent_change(_each_pattern[i], pattern[i])) > 350:
                    _should_skip = True
                    break
            # Only skips if one of the data points is too far out and doesn't meet the requirement
            if _should_skip:
                continue
            # If it all passes, then it appends the result of that array to the array that holds all the results
            _predicted_outcomes_array.append(self._performance_array[b])
        # returns that array
        return _predicted_outcomes_array

    def recognition(self, pattern):
        """
        This runs the recognition process on the current pattern
        :return: null
        """
        # This creates a start time to calculate how long it took to run recognition
        _start_time = time.time()
        _predicted_outcomes_array = self.analyse_pattern(pattern)

        # Calculates the number of patterns found from the returned array of previous outcomes
        _num_patterns_found = len(_predicted_outcomes_array)
        # If the number is greater than the required amount, it can continue
        if _num_patterns_found > self.constants.get_num_pattern_req():
            # It averages the outcome of all the numbers in the array to get an average outcome
            _predicted_avg_outcome = sum(_predicted_outcomes_array) / len(_predicted_outcomes_array)

            # It then decides whether the 'difference' is great enough to be worthy of a trade
            # Initialises the _option to N/A in case that there is not the required difference, it won't cause an error
            _option = enums.Option.NO_TRADE
            if _predicted_avg_outcome < -self.constants.get_required_difference():
                # SELLS
                _option = enums.Option.SELL
            elif _predicted_avg_outcome > self.constants.get_required_difference():
                # BUYS
                _option = enums.Option.BUY

            # If there has been a trade
            if _option != enums.Option.NO_TRADE:
                self._num_bets += 1
                print time.time() - _start_time
                return _option
            else:
                # No patterns have been found or criteria not met
                self.no_patterns(time.time() - _start_time)
                return None

        else:
            # No patterns have been found or criteria not met
            self.no_patterns(time.time() - _start_time)

    def no_patterns(self, final_time):
        """
        This is called when no patterns have been found or the criteria hasn't been  met so a standard input is
        sent to the log_handler class to insert into the database
        :param final_time: this is the time pattern recognition finished in (could be skewed if finishes early)
        :return: null
        """
        # Prints that there are no patterns and inserts the data into the db
        # print 'No patterns in: '.format(final_time)
        # self._log_handler.insert(num_patterns=None,
        #                          avg_predicted_outcome=None,
        #                          time_for_recog=final_time,
        #                          num_bets=None,
        #                          num_down_arrays=None,
        #                          num_up_arrays=None)

    def start(self):
        """
        This starts the pattern recognition by syncing with the server time and then
        running the recognition every minute from then on in order to trade
        :return:
        """
        print 'Pattern length: ', self.constants.get_pattern_len()
        print 'Required Difference: ', self.constants.get_required_difference()
        print 'Number patterns Req: ', self.constants.get_num_pattern_req()
        print 'Interval size: ', self.constants.get_interval_size()
        _num_loses = 0
        _num_draws = 0
        _num_no_bets = 0
        _num_wins = 0
        # Number of patterns there are
        max_iterations = len(self.pattern_data_tuples[0])
        print 'max_iterations: ', max_iterations
        index = 0
        while index < max_iterations-1:
            # Run recognition on the current pattern
            result = self.recognition(self.pattern_data_tuples[0][index])
            if result == enums.Option.NO_TRADE:
                _num_no_bets += 1
            else:
                if self.pattern_data_tuples[0][index] < self.pattern_data_tuples[0][index+1]:
                    if result == enums.Option.BUY:
                        _num_wins += 1
                    elif result == enums.Option.SELL:
                        _num_loses += 1
                elif self.pattern_data_tuples[0][index] > self.pattern_data_tuples[0][index+1]:
                    if result == enums.Option.BUY:
                        _num_loses += 1
                    elif result == enums.Option.SELL:
                        _num_wins += 1
                else:
                    _num_draws += 1
            if index % 10 == 0:
                print index
            index += 1
        total_num_bets = _num_wins + _num_draws + _num_loses
        percentage_win = float(float(_num_wins) / float(total_num_bets)) * 100
        percentage_lose = float(float(_num_loses) / float(total_num_bets)) * 100
        percentage_draw = float(float(_num_draws) / float(total_num_bets)) * 100
        print 'Percentage Win: {}%\nPercentage Lose: {}%\nPercentage Draw: {}%'\
            .format(percentage_win, percentage_lose, percentage_draw)
        return percentage_win, percentage_lose, percentage_draw

    # This is put in to avoid errors but I don't know why it is needed so leave it in
    if __name__ == '__main__':
        print 'this has been called by the __main__ thing which is bad'
