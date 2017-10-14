from math import sqrt


class BollingerBands:
    def __init__(self, constants_class, close_price):
        # This is the set of close prices
        self._all_close_prices = close_price
        # This is the constants class
        self._constants - constants_class
        # This is the sma period for the bollinger SMA
        self._bband_sma_period = self._constants.get_bollinger_band_sma_period()
        # This is the middle band
        self._middle_band = []
        # This is the standard deviation array
        self._bband_sd = []
        # This is the Upper Band
        self._upper_band = []
        # This is the Lower band
        self._lower_band = []
        # This is the Band width
        self._band_width = []

    def calculate_initial_sd_array(self):
        for i in range(len(self._sma_of_tp)):
            temp_list = self._typical_price_array[i:i + self._sma_period]
            self._standard_deviation_array.append(self.calculate_standard_deviation(temp_list))

    def calculate_standard_deviation(self, lst):
        """
        This calculates the standard deviation of a list of numbers
        :param lst: the list of numbers
        :return: the standard deviation (sqrt of variance)
        """
        num_items = len(lst)
        mean = sum(lst) / num_items
        return sqrt(sum([(x - mean) ** 2 for x in lst]) / (num_items - 1))
