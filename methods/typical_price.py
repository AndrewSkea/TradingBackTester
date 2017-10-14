from methods.sma import SMA
from math import sqrt

class TypicalPrice:
    def __init__(self, array_data_tuple, constants_class):
        # This is the global constants class
        self._constants = constants_class
        # This is the typical price array
        self._typical_price_array = []
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._high = array_data_tuple[4]
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._low = array_data_tuple[5]
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._close = array_data_tuple[6]
        # THis is the SMA class - This isn't set yet because we are passing in the data as a parameter to the class
        self._sma_class = None
        # This is the sma of the Typical Price
        self._sma_of_tp = []
        # This is the standard deviation array
        self._standard_deviation_array = []
        # This is the sma period (This must be the same as the CCI constant to it is taking it from that - no errors)
        self._sma_period = self._constants.get_cci_period()

    def add_to_data_arrays(self, close_value, high_value, low_value):
        self._high.append(high_value)
        self._low.append(low_value)
        self._close.append(close_value)

    def calculate_initial_array(self):
        for i in range(len(self._close)):
            self._typical_price_array.append((self._high[i] + self._close[i] + self._low[i]) / 3)

    def add_last_point(self, close_value, high_value, low_value):
        self.add_to_data_arrays(close_value, high_value, low_value)
        self._typical_price_array.append((close_value + high_value + low_value) / 3)

    def get_typical_price_array(self):
        return self._typical_price_array

    def get_last_point_in_typical_price_array(self):
        return self._typical_price_array[-1]

    def calculate_initial_sma_of_tp(self):
        self._sma_class = SMA(self._typical_price_array, self._sma_period)
        self._sma_class.calculate_initial_sma_array()
        self._sma_of_tp = self._sma_class.get_sma_array()

    def add_to_sma_array(self):
        self._sma_class.add_data_point(self._typical_price_array[-1])
        self._sma_of_tp = self._sma_class.get_sma_array()

    def get_sma_array_for_tp(self):
        return self._sma_of_tp

    def calculate_initial_sd_array(self):
        for i in range(len(self._sma_of_tp)):
            temp_list = self._typical_price_array[i:i + self._sma_period]
            self._standard_deviation_array.append(self.calculate_standard_deviation(temp_list))

    @staticmethod
    def calculate_standard_deviation(lst):
        """
        This calculates the standard deviation of a list of numbers
        :param lst: the list of numbers
        :return: the standard deviation (sqrt of variance)
        """
        num_items = len(lst)
        mean = sum(lst) / num_items
        return sqrt(sum([(mean - x) ** 2 for x in lst]) / (num_items - 1))

    def add_to_standard_deviation_array(self):
        temp_num = 0
        for j in range(-(self._sma_period + 1), -1, 1):
            temp_num += abs(self._sma_of_tp[-1] - self._typical_price_array[j])
        temp_num /= self._sma_period
        self._standard_deviation_array.append(temp_num)

    def get_standard_deviation_array_for_tp(self):
        return self._standard_deviation_array



