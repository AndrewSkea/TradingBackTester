from terminaltables import AsciiTable


class Constants:
    def __init__(self):
        """
        These are the base constant variable used throughout the program
        It is put in a class because for the back-testing, these variables get changed
        in order to try tweak them
        """
        ### THESE WILL CHANGE DURING THE PROCESS OF A GENETIC ALGORITHM TO TEST OPTIMAL NUMBERS FOR EACH ###
        # Length of the length of the pattern
        self._length_of_pattern = 30
        # Number of pattern required for a trade to happen
        self._num_pattern_req = 5000
        # Required difference of the predicted outcome to the last point in the array. Greater the better
        self._required_difference = 0.0001
        # The amount of patterns to skip every iteration to provide more variety
        self._interval_size = 1
        # Number of the live patterns we are using
        self._cut_off = 100
        # The period for ema 1 for the macd
        self._ema_a_period = 25
        # The period for ema 2 for the macd
        self._ema_b_period = 60
        # The signal period done on the macd
        self._signal_period = 15
        # This is the CCI period
        self._cci_period = 50
        # This is the CCI constant
        self._cci_constant = 0.015
        # This is the CCI limit
        self._cci_limit = 200
        # This is the typical price ema period
        self._typical_price_sma_period = 50
        # This is the sma period for the bollinger band
        self._bollinger_band_sma_period = 20

        ### THESE DON'T CHANGE DURING THE GENETIC ALGORITHM AS THEY ARE STATIC CONSTANTS, ONLY GETTERS ###
        # Number of the live patterns we are using (It will load always around 100 less than this number)
        self._num_live_patterns = 110000
        # Number of data points we use to compare the live patterns against
        self._num_data_points = 250000
        # Number of points the indicators have to run their ema and macd
        self._num_data_points_for_indicators = 50000
        # The decimal places the indicators round to (prevents too many calculations)
        self._indicator_num_decimal_points = 8

    def set_pattern_len(self, num):
        """
        Setter for the length of pattern
        :param num: the number to set it to
        :return: None
        """
        self._length_of_pattern = num

    def set_num_pattern_req(self, num):
        """
        The setter for the number of required patterns
        :param num: the number to set it to
        :return: None
        """
        self._num_pattern_req = num

    def set_required_difference(self, num):
        """
        The setter for the required difference for the patter recognition
        :param num: the number to set it to
        :return: None
        """
        self._required_difference = num

    def set_interval_size(self, num):
        """
        The setter for the interval size for going through patterns
        :param num: the number to set it to
        :return: None
        """
        self._interval_size = num

    def set_num_live_patterns(self, num):
        """
        The setter for the cut off point
        :param num: the number to set it to
        :return: None
        """
        self._num_live_patterns = num

    def set_num_data_points(self, num):
        """
        The setter for the number of data points to get from the database
        :param num: the number to set it to
        :return: None
        """
        self._num_data_points = num

    def set_num_data_points_for_indicators(self, num):
        """
        The setter for the number of data points that are taken from the database for the indicators
        :param num: the number to set it to
        :return: None
        """
        self._num_data_points = num

    def set_indicator_num_decimal_points(self, num):
        """
        The setter for the number of decimal points for the indicators
        :param num: the number to set it to
        :return: None
        """
        self._num_data_points = num

    # def set_num_live_patterns(self, num):
    #     """
    #     The setter for the cut off point
    #     :param num: the number to set it to
    #     :return: None
    #     """
    #     self._num_live_patterns = num
    #
    # def set_num_data_points(self, num):
    #     """
    #     The setter for the number of data points to get from the database
    #     :param num: the number to set it to
    #     :return: None
    #     """
    #     self._num_data_points = num
    #
    # def set_num_data_points_for_indicators(self, num):
    #     """
    #     The setter for the number of data points that are taken from the database for the indicators
    #     :param num: the number to set it to
    #     :return: None
    #     """
    #     self._num_data_points = num
    #
    # def set_indicator_num_decimal_points(self, num):
    #     """
    #     The setter for the number of decimal points for the indicators
    #     :param num: the number to set it to
    #     :return: None
    #     """
    #     self._num_data_points = num

    def set_ema_a_period(self, num):
        """
        The setter for the ema period number 1
        :param num: the number to set it to
        :return: None
        """
        self._ema_a_period = num

    def set_ema_b_period(self, num):
        """
        The setter for the ema period number 2
        :param num: the number to set it to
        :return: None
        """
        self._ema_b_period = num

    def set_signal_period(self, num):
        """
        The setter for the signal period
        :param num: the number to set it to
        :return: None
        """
        self._signal_period = num

    def set_cci_period(self, num):
        """
        The setter for the cci constant
        :param num: The number the cci constant will be set to
        :return:
        """
        self._cci_period = num

    def set_cci_constant(self, num):
        """
        The setter for the cci constant
        :param num: The number the cci constant will be set to
        :return:
        """
        self._cci_constant = num

    def set_typical_price_ema_period(self, num):
        """
        This is the typical price ema period
        :param num: The number to set it to
        :return: None
        """
        self._typical_price_sma_period = num

    def set_bollinger_band_sma_period(self, num):
        """
        This is the setter for the bollinger band sma period
        :param num: num to set it to
        :return: None
        """
        self._bollinger_band_sma_period = num

    def set_cci_limit(self, num):
        """
        The setter for the cci limit
        :param num:
        :return:
        """
        self._cci_limit = num

    def get_pattern_len(self):
        """
        The getter for the length of pattern
        :return: length of pattern constant
        """
        return self._length_of_pattern

    def get_num_pattern_req(self):
        """
        The getter for the number of pattern required
        :return: number patterns requierd constant
        """
        return self._num_pattern_req

    def get_required_difference(self):
        """
        The getter for the required difference for the patter recognition
        :return: The required differnce constant
        """
        return self._required_difference

    def get_interval_size(self):
        """
        The getter for the interval size for going through patterns
        :return: The interval size constant
        """
        return self._interval_size

    def get_num_live_patterns(self):
        """
        The getter for the number of live patterns
        :return: The number of live patterns constant
        """
        return self._num_live_patterns

    def get_num_data_points(self):
        """
        THe getter for the number of data points pulled from teh database
        :return: The number of data points constant
        """
        return self._num_data_points

    def get_num_data_points_for_indicators(self):
        """
        The number of data point for the indicators
        :return: The number of data points
        """
        return self._num_data_points

    def get_indicator_num_decimal_points(self):
        """
        The getter for the decimal points the n
        :return:
        """
        return self._num_data_points

    def get_ema_a_period(self):
        """
        This is the ema period a for the macd
        :return: The ema period
        """
        return self._ema_a_period

    def get_ema_b_period(self):
        """
        This is the ema period b for the macd
        :return: The ema period
        """
        return self._ema_b_period

    def get_signal_period(self):
        """
        This is the signal period a for the macd
        :return: The ema period
        """
        return self._signal_period

    def get_cci_constant(self):
        """
        This returns the cci constant
        :return: CCI Constant
        """
        return self._cci_constant

    def get_cci_period(self):
        """
        The setter for the cci constant
        :param num: The number the cci constant will be set to
        :return:
        """
        return self._cci_period

    def get_typical_price_sma_period(self):
        """
        This returns the typical price period for the ema
        :return:
        """
        return self._typical_price_sma_period

    def get_bollinger_band_sma_period(self):
        """
        This is the getter for the bollinger band sma period
        :return: bollinger band
        """
        return self._bollinger_band_sma_period

    def get_cci_limit(self):
        """
        The getter for the cci limit
        :return:
        """
        return self._cci_limit

    def get_genetic_algorithm_list_state(self):
        return [
            self.get_pattern_len(),
            self.get_num_pattern_req(),
            self.get_required_difference(),
            self.get_interval_size(),
            self.get_ema_a_period(),
            self.get_ema_b_period(),
            self.get_signal_period(),
            self.get_cci_period(),
            self.get_cci_constant(),
            self.get_typical_price_sma_period(),
            self.get_bollinger_band_sma_period(),
            self.get_cci_limit()
        ]

    def get_csv_str(self):
        """
        This return the csv format for the state on the constants class it is in right now
        :return: The CSV string
        """
        return '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
            self.get_pattern_len(),
            self.get_num_pattern_req(),
            self.get_required_difference(),
            self.get_interval_size(),
            self.get_num_live_patterns(),
            self.get_num_data_points(),
            self.get_num_data_points_for_indicators(),
            self.get_indicator_num_decimal_points(),
            self.get_ema_a_period(),
            self.get_ema_b_period(),
            self.get_signal_period(),
            self.get_cci_period(),
            self.get_cci_constant(),
            self.get_typical_price_sma_period(),
            self.get_bollinger_band_sma_period(),
            self.get_cci_limit())

    def get_str_table(self):
        table_data = [["Constant Name", "Value"]]
        table_data.append(["Pattern Length", self.get_pattern_len()])
        table_data.append(["Number Patterns required", self.get_num_pattern_req()])
        table_data.append(["Pattern difference required", self.get_required_difference()])
        table_data.append(["Interval size", self.get_interval_size()])
        table_data.append(["Number Live Patterns", self.get_num_live_patterns()])
        table_data.append(["Number data points", self.get_num_data_points()])
        table_data.append(["MACD EMA A period", self.get_ema_a_period()])
        table_data.append(["MACD EMA B period", self.get_ema_b_period()])
        table_data.append(["MACD Signal Period", self.get_signal_period()])
        table_data.append(["CCI Period", self.get_cci_period()])
        table_data.append(["CCI Constant", self.get_cci_constant()])
        table_data.append(["Typical Price SMA period", self.get_typical_price_sma_period()])
        table_data.append(["Bollinger Band SMA period", self.get_bollinger_band_sma_period()])
        table_data.append(["CCI Limit", self.get_cci_limit()])

        table = AsciiTable(table_data)
        return table.table
