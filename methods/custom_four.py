from enums.enums import Option, Position, Strength
from indicators import cci, rsi, bollingerbands, adx
from constants import finalconstants as const


class CustomFour:
    def __init__(self, data_array_class):
        """
        Combination of multiple CCIs using different time periods and constant values
        """
        self._data = data_array_class
        self.constants = const
        self.method_array = [
            cci.CCI(self._data, upper_limit=225, lower_limit=190, period=22, time_limits=[(17, 19)]),
            cci.CCI(self._data, upper_limit=250, lower_limit=220, period=22, time_limits=[(12, 19)]),
            # bollingerbands.BollingerBands(self._data, period=22, upper_stdev_multiplier=3,
            #                               lower_stdev_multiplier=3.5, time_limits=[(13, 18)]),
        ]
        self.adx_method = adx.ADX(self._data, period=18, time_limits=[(0, 10)])

    def update_data_arrays(self):
        [method.update_data_arrays() for method in self.method_array]
        self.adx_method.update_data_arrays()

    def get_result(self):
        for method in self.method_array[:2]:
            if method.is_trading_time() and self.adx_method.get_strength_of_trend() == Strength.MILD:
                if method.has_broken_out() == Position.JUST_GONE_ABOVE:
                    return Option.SELL
                elif method.has_broken_out() == Position.JUST_GONE_BELOW:
                    return Option.BUY
        return Option.NO_TRADE
