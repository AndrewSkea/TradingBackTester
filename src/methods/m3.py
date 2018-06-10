from enums.enums import Option, Position
from indicators import bollingerbands, rsi, ema
from constants import finalconstants as const


class CustomMethod:
    def __init__(self, data_array_class):
        """
        Combination of multiple CCIs using different time periods and constant values
        """
        self._data = data_array_class
        self.constants = const
        self.bband = bollingerbands.BollingerBands(self._data, period=25, upper_stdev_multiplier=2.4,
                                                   lower_stdev_multiplier=2.2, time_limits=[(16, 19)])
        self.rsi_method = rsi.RSI(self._data, period=22, upper_limit=80, lower_limit=20, time_limits=[(16, 19)])
        self.ema = ema.EMA(3)

    def update_data_arrays(self):
        self.rsi_method.update_data_arrays()
        self.bband.update_data_arrays()
        self.ema.add_data_point(self.rsi_method.rsi[-1])

    def get_result(self):
        if self.bband.has_broken_out() == Position.JUST_GONE_ABOVE and 77 < self.ema.get_ema_array()[-1]:
            return Option.SELL
        elif self.bband.has_broken_out() == Position.JUST_GONE_BELOW and 22 > self.ema.get_ema_array()[-1]:
            return Option.BUY
        return Option.NO_TRADE
