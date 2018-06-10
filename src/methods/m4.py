from enums.enums import Option, Position
from indicators import cci, bollingerbands, rsi


class CustomMethod:
    def __init__(self, data_array_class):
        """
        Combination of multiple CCIs using different time periods and constant values
        """
        self._data = data_array_class
        time_limits = [(0, 9), (15, 23)]
        self.bband = bollingerbands.BollingerBands(self._data, period=24, upper_stdev_multiplier=2.1,
                                                   lower_stdev_multiplier=2.4, time_limits=time_limits)
        self.rsi_method = rsi.RSI(self._data, period=25, upper_limit=76, lower_limit=23, time_limits=time_limits)

    def update_data_arrays(self):
        self.rsi_method.update_data_arrays()
        self.bband.update_data_arrays()

    def get_result(self):
        if self.bband.is_trading_time():
            if self.bband.has_broken_out() == Position.JUST_GONE_ABOVE and self.rsi_method.is_outside() == Position.ABOVE:
                return Option.SELL
            elif self.bband.has_broken_out() == Position.JUST_GONE_BELOW and self.rsi_method.is_outside() == Position.BELOW:
                return Option.BUY
        return Option.NO_TRADE
