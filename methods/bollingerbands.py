from math import sqrt
from methods import sma
from enums.enums import Option

class BollingerBands:
    def __init__(self, close_price, constants_class):
        # This is the set of close prices
        self._all_close_prices = close_price
        # This is the constants class
        self._constants = constants_class
        # This is the sma period for the bollinger SMA
        self._bband_sma_period = self._constants.get_bollinger_band_sma_period()
        # This is the Middle Band SMA class
        self._middle_band_sma = sma.SMA(self._all_close_prices, self._bband_sma_period)
        # This is the middle band
        self._middle_band = []
        # This is the SMA for the Upper Band
        self._upper_band_sma = sma.SMA(self._all_close_prices, self._bband_sma_period)
        # This is the Upper Band
        self._upper_band = []
        # This is the lower band sma class
        self._lower_band_sma = sma.SMA(self._all_close_prices, self._bband_sma_period)
        # This is the Lower band
        self._lower_band = []
        # This is the standard deviation array
        self._bband_sd = []
        # This is the Band width
        self._band_width = []

    def calculate_initial_arrays(self):
        self._middle_band_sma.get_sma_array()
        self._middle_band = self._middle_band_sma.get_sma_array()
        self.calculate_lower_band()
        self.calculate_upper_band()
        self.calculate_band_width_array()

    def calculate_initial_sd_array(self):
        for i in range(len(self._middle_band)):
            temp_list = self._all_close_prices[i:i + self._bband_sma_period]
            self._bband_sd.append(self.calculate_standard_deviation(temp_list))

    def calculate_standard_deviation(self, lst):
        """
        This calculates the standard deviation of a list of numbers
        :param lst: the list of numbers
        :return: the standard deviation (sqrt of variance)
        """
        num_items = len(lst)
        mean = sum(lst) / num_items
        return sqrt(sum([(x - mean) ** 2 for x in lst]) / (num_items - 1))

    def calculate_upper_band(self):
        for i in range(len(self._middle_band)):
            self._upper_band.append(self._middle_band[i] + self._bband_sd[i] * 2)

    def calculate_lower_band(self):
        for i in range(len(self._middle_band)):
            self._lower_band.append(self._middle_band[i] - self._bband_sd[i] * 2)

    def calculate_band_width_array(self):
        for i in range(len(self._middle_band)):
            self._band_width.append(abs(self._upper_band[i] - self._lower_band[i]))

    def add_to_arrays(self, close_value):
        # Add to the Middle Band SMA
        self._all_close_prices.append(close_value)
        self._middle_band_sma.add_data_point(close_value)
        self._middle_band = self._middle_band_sma.get_sma_array()

        # Add to the Standard Deviation array
        self._bband_sd.append(self.calculate_standard_deviation(self._all_close_prices[-self._bband_sma_period:]))

        # Add to Upper Band Array
        self._upper_band.append(self._middle_band[-1] + self._bband_sd[-1] * 2)

        # Add to Lower Band array:
        self._lower_band.append(self._middle_band[-1] - self._bband_sd[-1] * 2)

        # Add to the Band width array
        self._band_width.append(abs(self._upper_band[-1] - self._lower_band[-1]))

    def get_result(self):
        # print 'Band width: ', self._band_width[-1]
        # NEED TO DO THIS
        return Option.NO_TRADE

