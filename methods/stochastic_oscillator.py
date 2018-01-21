from enums.enums import Option

class StochasticOscillator:
    """
    This is the Stoch Osc class
    """

    def __init__(self, high_price, low_price, close_price, constant_class):
        # This is the Stoch osc array
        self._stoch_osc_array = []
        # THis is the constants class
        self._constant_class = constant_class
        # Highest high array
        self._highest_high_array = []
        # Lowest low array
        self._lowest_low_array = []
        # Historic Data arrays
        self._high_prices = list(high_price)
        self._low_prices = list(low_price)
        self._close_prices = list(close_price)
        # Stochastic Oscillator period
        self._period = self._constant_class.get_stochastic_oscillator_period()

    def add_to_stoch(self, high, low, close):
        self._high_prices.append(high)
        self._low_prices.append(low)
        self._close_prices.append(close)
        try:
            if len(self._highest_high_array) > self._period:
                self._highest_high_array.append(max(self._high_prices[-self._period:]))
                self._lowest_low_array.append(min(self._low_prices[-self._period:]))
            else:
                self._highest_high_array.append(max(self._high_prices))
                self._lowest_low_array.append(min(self._low_prices))
            self._stoch_osc_array.append(
                    (self._close_prices[-1] - self._lowest_low_array[-1]) /
                    (self._highest_high_array[-1] - self._lowest_low_array[-1])
                    * 100)
        except ZeroDivisionError:
            print("Dividing by zero")

    def get_result(self):
        try:
            result_array = []
            for num in range(-3, 0, 1):
                if self._stoch_osc_array[num] > 70:
                    result_array.append(Option.SELL)
                elif self._stoch_osc_array[num] < 30:
                    result_array.append(Option.BUY)
                else:
                    result_array.append(Option.NO_TRADE)

            if result_array.count(Option.BUY) >= 3:
                return Option.BUY
            elif result_array.count(Option.SELL) >= 3:
                return Option.SELL
            else:
                return Option.NO_TRADE
        except IndexError:
            return Option.NO_TRADE