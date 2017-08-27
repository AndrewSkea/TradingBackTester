from methods import percentage_change
from constants import constants
import time


class Loader:
    """
    This is the pattern loader class. It takes all the data from the db
    and turns it into 4 different arrays that make it easier for the
    recognition to process
    """

    def __init__(self, all_data):
        """
        Initialises the base variables for the class
        :param all_data: This is the array of all the data that is taken from the histdata table in the db
        :param constants.length_of_pattern: This is the global length of pattern used by all classes
        """
        # This is all the data taken from the database
        self._all_data = all_data
        # The size of the array that holds all the data i.e. How many data points there are
        self._all_data_length = len(self._all_data)

        # Initialising the arrays
        # The buy pattern array is the set of arrays where the outcome has been higher (i.e. should buy)
        self._buy_pattern_array = []
        # The performance array is the outcome. It has the same index as it's relative pattern in the pattern array
        self._buy_performance_array = []
        # The sell pattern array is the set of arrays where the outcome is lower than (i.e. should sell)
        self._sell_pattern_array = []
        # The sell performance array is the set of outcomes for the sell pattern array
        self._sell_performance_array = []

    def pattern_storage(self):
        """
        This uses the full data set to split it into the 4 different arrays described above
        :return: tuple of the 4 different arrays
        """
        _start_time = time.time()
        # This is the data length that is going to be used so tht it doesn't go until the end because there
        # won't be any data +30 points in the future then
        _used_data_length = int(self._all_data_length - (2 * (constants.length_of_pattern-1))/constants._interval_size)
        _current_index = constants.length_of_pattern
        # Goes through all the data to get the percentage change through all of it
        while _current_index < _used_data_length:
            pattern = []
            for i in range(constants.length_of_pattern - 2, -1, -1):
                pattern.append(percentage_change.percent_change(
                    self._all_data[_current_index - constants.length_of_pattern + 1],
                    self._all_data[_current_index - i]))

            _outcome_range = self._all_data[_current_index+1]
            _current_point = self._all_data[_current_index]
            _future_outcome = percentage_change.percent_change(_current_point, _outcome_range)

            if pattern[1] >= pattern[0]:
                self._buy_pattern_array.append(pattern)
                self._buy_performance_array.append(_future_outcome)
            else:
                self._sell_pattern_array.append(pattern)
                self._sell_performance_array.append(_future_outcome)

            _current_index += 1
        print 'Time for recognition: ', time.time() - _start_time
        # print len(self._buy_pattern_array)
        # print len(self._buy_performance_array)
        # print len(self._sell_pattern_array)
        # print len(self._sell_performance_array)
        return (self._buy_pattern_array, self._buy_performance_array,
                self._sell_pattern_array, self._sell_performance_array)


