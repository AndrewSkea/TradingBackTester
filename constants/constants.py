
class Constants:
    def __init__(self):
        """
        These are the base constant variable used throughout the program
        It is put in a class because for the back-testing, these variables get changed
        in order to try tweak them
        """
        # Length of the length of the pattern
        self._length_of_pattern = 30
        # Number of pattern required for a trade to happen
        self._num_pattern_req = 2000
        # Required difference of the predicted outcome to the last point in the array. Greater the better
        self._required_difference = 0.000075
        # The amount of patterns to skip every iteration to provide more variety
        self._interval_size = 1
        # Number of the live patterns we are using
        self._cut_off = 100
        # Number of data points we use to compare the live patterns against
        self._max_num_data_points = 250000
        self._num_data_points_for_indicators = 50000
        self._indicator_num_decimal_points = 8
        self._ema_a_period = 12
        self._ema_b_period = 26
        self._signal_period = 9

    def set_pattern_len(self, num):
        self._length_of_pattern = num

    def set_num_pattern_req(self, num):
        self._num_pattern_req = num

    def set_required_difference(self, num):
        self._required_difference = num

    def set_interval_size(self, num):
        self._interval_size = num

    def set_cut_off(self, num):
        self._cut_off = num

    def set_max_num_data_points(self, num):
        self._max_num_data_points = num

    def set_num_data_points_for_indicators(self, num):
        self._max_num_data_points = num

    def set_indicator_num_decimal_points(self, num):
        self._max_num_data_points = num

    def set_ema_a_period(self, num):
        self._ema_a_period = num

    def set_ema_b_period(self, num):
        self._ema_b_period = num

    def set_signal_period(self, num):
        self._signal_period = num

    def get_pattern_len(self):
        return self._length_of_pattern

    def get_num_pattern_req(self):
        return self._num_pattern_req

    def get_required_difference(self):
        return self._required_difference

    def get_interval_size(self):
        return self._interval_size

    def get_cut_off(self):
        return self._cut_off

    def get_max_num_data_points(self):
        return self._max_num_data_points

    def get_num_data_points_for_indicators(self):
        return self._max_num_data_points

    def get_indicator_num_decimal_points(self):
        return self._max_num_data_points

    def get_ema_a_period(self):
        return self._ema_a_period

    def get_ema_b_period(self):
        return self._ema_b_period

    def get_signal_period(self):
        return self._signal_period

    def get_csv_str(self):
        return '{},{},{},{},{},{},{},{},{},{},{}'.format(
            self.get_pattern_len(),
            self.get_num_pattern_req(),
            self.get_required_difference(),
            self.get_interval_size(),
            self.get_cut_off(),
            self.get_max_num_data_points(),
            self.get_num_data_points_for_indicators(),
            self.get_indicator_num_decimal_points(),
            self.get_ema_a_period(),
            self.get_ema_b_period(),
            self.get_signal_period())


