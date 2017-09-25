from methods.typical_price import TypicalPrice


class CCI:
    """
    This is the CCI class that takes calculates, and provides CCI data on the patterns
    """

    def __init__(self, data_point_tuples, constant_class):
        # This is the CCI array
        self._cci_array = []
        # THis is the constants class
        self._constant_class = constant_class
        # This is the CCI constant (normally 0.015 on the internet)
        self._cci_constant = self._constant_class.get_cci_constant()
        # This is the period for the CCI class
        self._cci_period = self._constant_class.get_cci_period()
        # This is the Typical Price array class that this class will use
        self._tp_class = TypicalPrice(data_point_tuples, self._constant_class)
        self._tp_array = self._tp_class.calculate_initial_array()
        self._tp_sma_array = self._tp_class.calculate_initial_sma_of_tp()
        self._sd_array = self._tp_class.calculate_initial_sd_array()

    def calculate_cci_initial_array(self):
        for i in range(len(self._sd_array)):
            self._cci_array.append((self._tp_array[i + self._cci_period] - self._tp_sma_array[i]) /
                                   (self._cci_constant * self._sd_array[i]))

    def add_to_cci_array(self, close, high, low):
        self._tp_class.add_last_point(close, high, low)
        self._tp_class.add_to_sma_array()
        self._tp_class.add_to_standard_deviation_array()
        self._cci_array.append((self._tp_array[-1] - self._tp_sma_array[-1])/(self._cci_constant * self._sd_array[-1]))

    def get_cci_array_(self):
        return self._cci_array

    def get_result(self):
        return self._cci_array[-1]
