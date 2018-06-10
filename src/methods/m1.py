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
        self.method_array = [
            cci.CCI(self._data, upper_limit=225, lower_limit=200, period=22, time_limits=[(17, 19)]),
            cci.CCI(self._data, upper_limit=235, lower_limit=220, period=22, time_limits=[(17, 19)])
        ]

    def update_data_arrays(self):
        [method.update_data_arrays() for method in self.method_array]

    def get_result(self):
        for method in self.method_array[:2]:
            if method.is_trading_time():
                if method.has_broken_out() == Position.JUST_GONE_ABOVE:
                    return Option.SELL
                elif method.has_broken_out() == Position.JUST_GONE_BELOW:
                    return Option.BUY
        return Option.NO_TRADE
