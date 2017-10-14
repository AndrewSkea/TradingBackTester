from methods.typical_price import TypicalPrice
from enums.enums import Option
import time

class CCI:
    """
    This is the CCI class that takes calculates, and provides CCI data on the patterns
    """

    def __init__(self, high_price, low_price, close_price, constant_class):
        # This is the CCI array
        self._cci_array = []
        # THis is the constants class
        self._constant_class = constant_class
        # This is the CCI constant (normally 0.015 on the internet)
        self._cci_constant = self._constant_class.get_cci_constant()
        # Get the CCI limit constant
        self._cci_limit = self._constant_class.get_cci_limit()
        # This is the period for the CCI class
        self._cci_period = self._constant_class.get_cci_period()
        # This is the Typical Price array class that this class will use
        self._tp_class = TypicalPrice(high_price, low_price, close_price, self._constant_class)
        # This makes the tp class calculate the initial tp array
        self._tp_class.calculate_initial_array()
        self._tp_array = self._tp_class.get_typical_price_array()
        # This makes the tp class calculate the sma array for the tp
        self._tp_class.calculate_initial_sma_of_tp()
        self._tp_sma_array = self._tp_class.get_sma_array_for_tp()
        # This makes the tp class calculate the standard deviation array for the tp class
        self._tp_class.calculate_initial_md_array()
        self._md_array = self._tp_class.get_standard_deviation_array_for_tp()

    def calculate_cci_initial_array(self):
        """
        This calculates the cci initial array
        :return:
        """
        for i in range(len(self._md_array)):
            try:
                self._cci_array.append((self._tp_array[i + self._cci_period] - self._tp_sma_array[i]) /
                                       (self._cci_constant * self._md_array[i]))
            except IndexError:
                print 'Index Error at index: ', i

    def add_to_cci_array(self, close, high, low):
        tp, sma, dev = self._tp_class.add_last_point(close, high, low)
        self._cci_array.append((tp - sma) /
                               (self._cci_constant * dev))

    def update_arrays(self):
        self._tp_array = self._tp_class.get_typical_price_array()
        self._tp_sma_array = self._tp_class.get_sma_array_for_tp()
        self._md_array = self._tp_class.get_standard_deviation_array_for_tp()

    def get_cci_array_(self):
        return self._cci_array

    def get_result(self):
        option = Option.NO_TRADE
        if int(self._cci_array[-1]) > self._cci_limit:
            option = Option.SELL
        elif int(self._cci_array[-1]) < -self._cci_limit:
            option = Option.BUY
        return option, 0

    def get_amount_of_consecutive_times_cci_is_overtraded(self):
        """
        This returns the amount times the cci has been overtraded. So, if the last few values have been under -100 or
        above 100, it counts the amount of times, this has happened and returns the value
        :return: The number of consecutive times the cci has been over traded
        """
        if self._cci_array[-1] < -100:
            for i in range(len(self._cci_array)):
                if self._cci_array[-i] < -100:
                    continue
                else:
                    return i
        elif self._cci_array[-1] > 100:
            for i in range(len(self._cci_array)):
                if self._cci_array[-i] > 100:
                    continue
                else:
                    return i
        else:
            return 0
