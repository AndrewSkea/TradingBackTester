from methods.typical_price import TypicalPrice
from enums.enums import Option, Trend


def percent_change(_start_point, _current_point):
    try:
        if _start_point > _current_point:
            x = -((float(_start_point) - float(_current_point)) / abs(_current_point)) * 100
        else:
            x = ((float(_current_point) - float(_start_point)) / abs(_start_point)) * 100
        if x == 0.0:
            return 0.000000001
        else:
            return x
    except:
        return 0.000000001


class CCI:
    """
    This is the CCI class that takes calculates, and provides CCI data on the patterns
    """

    def __init__(self, high_price, low_price, close_price, constant_class):
        self._close_array = list(close_price)
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
        self._tp_class = TypicalPrice(list(high_price), list(low_price), list(close_price), self._constant_class)
        # This makes the tp class calculate the initial tp array
        self._tp_array = self._tp_class.get_typical_price_array()
        # This makes the tp class calculate the sma array for the tp
        self._tp_sma_array = self._tp_class.get_sma_array_for_tp()
        # This makes the tp class calculate the standard deviation array for the tp class
        self._tp_class.calculate_initial_md_array()
        self._md_array = self._tp_class.get_standard_deviation_array_for_tp()
        self._trend_index = 0
        # MAKE SURE THIS IS DIVISIBLE BY 4
        self._trend_length = 12
        # Percentage change period
        self._pc_period = 20
        # Percentage change array for CCI
        self._pc_cci = []

    def send_results_to_graph(self, graph1, future_close_point, title_text):
        self.update_arrays()
        if len(self._cci_array) > 50:
            graph1.start(self._tp_array, [], self._tp_sma_array,
                         self._close_array, [], future_close_point, title_text)

    def add_to_cci_array(self, close, high, low):
        self._close_array.append(close)
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
        limit = 100
        if self._cci_array[-1] > limit and self._cci_array[-2] > limit and self._cci_array[-3] > limit:
            return Option.SELL, 0
        elif self._cci_array[-1] < -limit and self._cci_array[-2] < -limit and self._cci_array[-3] < -limit:
            return Option.BUY, 0
        elif self._cci_array[-1] > limit > self._cci_array[-2] > self._cci_array[-3]:
            return Option.BUY, 0
        elif self._cci_array[-1] < -limit < self._cci_array[-2] < self._cci_array[-3]:
            return Option.SELL, 0

        return Option.NO_TRADE, 0

