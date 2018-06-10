from .sma import SMA
from ..functions.mean_deviation import calculate_mean_deviation


class TypicalPrice:
    def __init__(self, constants_class):
        # This is the global constants class
        self._constants = constants_class
        # This is the typical price array
        self._typical_price_array = []
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._high = []
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._low = []
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._close = []
        # This is the SMA class - This isn't set yet because we are passing in the data as a parameter to the class
        self._sma_class = SMA(20)
        # This is the sma of the Typical Price
        self._sma_of_tp = []
        # This is the standard deviation array
        self._mean_deviation_array = []
        # This is the sma period (This must be the same as the CCI constant to it is taking it from that - no errors)
        self._sma_period = self._constants.get_cci_period()

    def add_to_data_arrays(self, close_value, high_value, low_value):
        self._high.append(high_value)
        self._low.append(low_value)
        self._close.append(close_value)

    def add_last_point(self, close_value, high_value, low_value):
        self.add_to_data_arrays(close_value, high_value, low_value)
        tp = (close_value + high_value + low_value) / 3
        self._typical_price_array.append(tp)
        self.add_to_sma_array(tp)
        self.add_to_mean_deviation_array()
        return tp, self._sma_of_tp[-1], self._mean_deviation_array[-1]

    def get_typical_price_array(self):
        return self._typical_price_array

    def get_last_point_in_typical_price_array(self):
        return self._typical_price_array[-1]

    def add_to_sma_array(self, tp):
        self._sma_class.add_data_point(tp)
        self._sma_of_tp = self._sma_class.get_sma_array()

    def get_sma_array_for_tp(self):
        return self._sma_of_tp

    def calculate_initial_md_array(self):
        for i in range(len(self._sma_of_tp)):
            self._mean_deviation_array.append(
                calculate_mean_deviation(self._typical_price_array[i:i + self._sma_period], self._sma_of_tp[i]))

    def add_to_mean_deviation_array(self):
        self._mean_deviation_array.append(
            calculate_mean_deviation(self._typical_price_array[-self._sma_period:], self._sma_of_tp[-1]))

    def get_standard_deviation_array_for_tp(self):
        return self._mean_deviation_array
