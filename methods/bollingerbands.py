from math import sqrt
from methods import sma
from enums.enums import Option

class BollingerBands:
    def __init__(self, high_prices, low_prices, close_prices, constants_class):
        # This is the set of close prices
        self._all_close_prices = list(close_prices)
        # This is the set of low prices
        self._all_low_prices = list(low_prices)
        # This is the set of high prices
        self._all_high_prices = list(high_prices)
        # This is the constants class
        self._constants = constants_class
        # This is the sma period for the bollinger SMA
        self._bband_sma_period = self._constants.get_bollinger_band_sma_period()
        # This is the Middle Band SMA class
        self._middle_band_sma = sma.SMA(self._bband_sma_period)
        # This is the middle band
        self._middle_band = []
        # # This is the SMA for the Upper Band
        # self._upper_band_sma = sma.SMA(self._all_close_prices, self._bband_sma_period)
        # This is the Upper Band
        self._upper_band = []
        # # This is the lower band sma class
        # self._lower_band_sma = sma.SMA(self._all_close_prices, self._bband_sma_period)
        # This is the Lower band
        self._lower_band = []
        # This is the standard deviation array
        self._bband_sd = []
        # This is the Band width
        self._band_width = []

    def calculate_standard_deviation(self, lst):
        """
        This calculates the standard deviation of a list of numbers
        :param lst: the list of numbers
        :return: the standard deviation (sqrt of variance)
        """
        num_items = len(lst)
        mean = sum(lst) / num_items
        try:
            num = sqrt(sum([(x - mean) ** 2 for x in lst]) / (num_items - 1))
        except ZeroDivisionError:
            num = 0
        return num

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

    def send_results_to_graph(self, graph1, future_close_point, title_text):
        if len(self._upper_band) > 50:
            graph1.start(self._upper_band, self._all_close_prices, self._lower_band,
                         self._middle_band, [], future_close_point, title_text)

    def get_result(self):
        try:
            result_array = []
            for num in range(-3, 0, 1):
                if self._all_close_prices[num] < self._lower_band[num]:
                    result_array.append(Option.BUY)
                elif self._all_close_prices[num] > self._upper_band[num]:
                    result_array.append(Option.SELL)
                elif self._all_high_prices[num] > self._upper_band[num] > self._all_close_prices[num]:
                    result_array.append(Option.SELL)
                elif self._all_low_prices[num] < self._lower_band[num] < self._all_close_prices[num]:
                    result_array.append(Option.BUY)
                else:
                    result_array.append(Option.NO_TRADE)

            if result_array.count(Option.BUY) >= 3:
                return Option.BUY
            elif result_array.count(Option.SELL) >= 3:
                return Option.SELL
            else:
                return Option.NO_TRADE
        except IndexError:
            return Option.NO_TRADE

