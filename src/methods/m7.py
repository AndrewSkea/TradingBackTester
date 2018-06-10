from enums.enums import Option
from indicators import cci


class CustomMethod:
    def __init__(self, data_array_class):
        """
        Combination of multiple CCIs using different time periods and constant values
        """
        self._data = data_array_class
        time_limits = [(13, 21)]
        self.cci_method = cci.CCI(self._data, period=24, upper_limit=220, lower_limit=220, time_limits=time_limits)

    def update_data_arrays(self):
        self.cci_method.update_data_arrays()

    def get_result(self):
        if self.cci_method.is_trading_time():
            if self.cci_method.has_broken_above() and self.cci_method.has_moved_up_for():
                return Option.SELL
            elif self.cci_method.has_broken_below() and self.cci_method.has_moved_down_for():
                    return Option.BUY
        return Option.NO_TRADE
