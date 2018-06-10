from enums.enums import Option, Position
from indicators import cci, bollingerbands, rsi
from constants import finalconstants as const


class CustomMethod:
    def __init__(self, data_array_class):
        """
        Combination of multiple CCIs using different time periods and constant values
        """
        self._data = data_array_class
        self.constants = const
        self.bband = bollingerbands.BollingerBands(self._data, period=22, upper_stdev_multiplier=2.5,
                                                   lower_stdev_multiplier=2.5, time_limits=[(17, 19)])
        self.cci_method = cci.CCI(self._data, upper_limit=180, lower_limit=180, period=17, time_limits=[(17, 19)])

    def update_data_arrays(self):
        self.cci_method.update_data_arrays()
        self.bband.update_data_arrays()

    def get_result(self):
        if self.bband.is_trading_time():
            if self.cci_method.has_broken_out() == Position.JUST_GONE_ABOVE and \
                            self.bband.is_outside() == Position.ABOVE:
                return Option.SELL
            elif self.cci_method.has_broken_out() == Position.JUST_GONE_BELOW and \
                            self.bband.is_outside() == Position.BELOW:
                return Option.BUY
        return Option.NO_TRADE
