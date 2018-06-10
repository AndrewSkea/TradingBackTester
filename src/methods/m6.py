from enums.enums import Option, Position, Trend
from indicators import adx, bollingerbands, rsi


class CustomMethod:
    def __init__(self, data_array_class):
        """
        Combination of multiple CCIs using different time periods and constant values
        """
        self._data = data_array_class
        time_limits = [(13, 20)]
        self.bband = bollingerbands.BollingerBands(self._data, period=23, upper_stdev_multiplier=2.7,
                                                   lower_stdev_multiplier=2.9, time_limits=time_limits)
        self.rsi_method = rsi.RSI(self._data, period=12, upper_limit=75, lower_limit=25, time_limits=time_limits)
        self.adx_method = adx.ADX(self._data, period=12, time_limits=time_limits)

    def update_data_arrays(self):
        self.rsi_method.update_data_arrays()
        self.bband.update_data_arrays()
        self.adx_method.update_data_arrays()

    def get_result(self):
        if self.adx_method.get_strength_value() < 30:
            if self.bband.has_broken_out() == Position.JUST_GONE_ABOVE and self.rsi_method.is_outside() == Position.ABOVE and \
                            self.rsi_method.moving_in_direction_for(4) == Trend.UP:
                return Option.SELL
            elif self.bband.has_broken_out() == Position.JUST_GONE_BELOW and self.rsi_method.is_outside() == Position.BELOW and \
                            self.rsi_method.moving_in_direction_for(4) == Trend.DOWN:
                return Option.BUY
        return Option.NO_TRADE
