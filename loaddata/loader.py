from methods.percentage_change import percent_change
import time

class Loader:
    """
    This is the pattern loader class. It takes all the data from the db
    and turns it into 4 different arrays that make it easier for the
    recognition to process
    """

    def __init__(self, all_data, constants_class):
        """
        Initialises the base variables for the class
        :param all_data: This is the array of all the data that is taken from the histdata table in the db
        :param constants.length_of_pattern: This is the global length of pattern used by all classes
        """
        self.constants = constants_class
        self._all_data = all_data
        self._close_prices_for_loading = []
        # This is all the close prices of the database
        for i in all_data:
            self._close_prices_for_loading.append(i[-1])
        # The size of the array that holds all the data i.e. How many data points there are
        self._all_data_length = len(self._close_prices_for_loading)
        # Initialising the arrays
        # Percentage Change pattern array
        self._pattern_array = []
        # The performance array, i,e, what the outcome was (percentage change from the starting value too)
        self._performance_array = []
        self._time = []
        self._open_price = []
        self._high_price = []
        self._low_price = []
        self._close_price = []

    def pattern_storage(self):
        """
        This uses the full data set to split it into the 4 different arrays described above
        :return: tuple of the 7 different arrays
        """
        _start_time = time.time()
        # This is the data length that is going to be used so tht it doesn't go until the end because there
        # won't be any data +30 points in the future then
        _used_data_length = int(int(self._all_data_length - (2 * (self.constants.get_pattern_len()-1))) / self.constants.get_interval_size())
        _current_index = self.constants.get_pattern_len()
        # Goes through all the data to get the percentage change through all of it
        while _current_index < _used_data_length:
            pattern = []
            for i in range(self.constants.get_pattern_len() - 2, -1, -1):
                pattern.append(percent_change(
                    self._close_prices_for_loading[_current_index - self.constants.get_pattern_len() + 1],
                    self._close_prices_for_loading[_current_index - i]))

            _outcome_range = self._close_prices_for_loading[_current_index + 1]
            _current_point = self._close_prices_for_loading[_current_index]
            _future_outcome = percent_change(_current_point, _outcome_range)

            self._pattern_array.append(pattern)
            self._performance_array.append(_future_outcome)
            self._time.append(self._all_data[_current_index][1])
            self._open_price.append(self._all_data[_current_index][2])
            self._high_price.append(self._all_data[_current_index][3])
            self._low_price.append(self._all_data[_current_index][4])
            self._close_price.append(self._all_data[_current_index][5])

            _current_index += 1

        print '{} patterns processed in {} s'.format(len(self._pattern_array), time.time() - _start_time)

        return (self._pattern_array, self._performance_array, self._time, self._open_price, self._high_price,
                self._low_price, self._close_price)


