from enums.enums import Option, Position, Strength
from indicators import rsi, stochastic_oscillator, adx
from constants import finalconstants as const


class CustomMethod:
    def __init__(self, data_array_class):
        """
        Combination of multiple CCIs using different time periods and constant values
        """
        self._data = data_array_class
        self.constants = const
        self.adx_method = adx.ADX(self._data, period=18, time_limits=[(9, 20)])
        # self.rsi_method = rsi.RSI(self._data, period=14, upper_limit=80, lower_limit=20, time_limits=[(9, 20)])
        self.stoch_method = stochastic_oscillator.StochasticOscillator(self._data, 15, 3, 80, 20, time_limits=[(9, 20)])

    def update_data_arrays(self):
        self.adx_method.update_data_arrays()
        # self.rsi_method.update_data_arrays()
        self.stoch_method.update_data_arrays()

    def get_result(self):
        if self.stoch_method.is_trading_time():
            if self.adx_method.get_strength_of_trend() == Strength.STRONG:
                if self.stoch_method.is_outside() == Position.ABOVE and \
                                self.stoch_method.has_crossed_over() == Position.JUST_GONE_BELOW:
                    return Option.SELL
                if self.stoch_method.is_outside() == Position.BELOW and \
                                self.stoch_method.has_crossed_over() == Position.JUST_GONE_ABOVE:
                    return Option.BUY
        return Option.NO_TRADE
