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
        self._high_prices = high_price
        self._low_prices = low_price
        self._close_prices = close_price
        # Stochastic Oscillator period
        self._period = self._constant_class.get_stochastic_oscillator_period()

    def calculate_stoch_osc_initial_array(self):
        self.calculate_initial_high_and_low_arrays()
        for i in range(self._period, len(self._close_prices), 1):
            j = i - self._period
            self._stoch_osc_array.append(
                (self._close_prices[i] - self._lowest_low_array[j]) /
                (self._highest_high_array[j] - self._lowest_low_array[j])
                * 100)

    def calculate_initial_high_and_low_arrays(self):
        for i in range(self._period, len(self._high_prices), 1):
            self._highest_high_array.append(max(self._high_prices[i-self._period:i]))
            self._lowest_low_array.append(min(self._low_prices[i-self._period:i]))

    def add_to_stoch(self, high, low, close):
        self._high_prices.append(high)
        self._lowest_low_array.append(low)
        self._close_prices.append(close)

        self._highest_high_array.append(max(self._high_prices[self._period:]))
        self._lowest_low_array.append(min(self._low_prices[self._period:]))
        self._stoch_osc_array.append(
                (self._close_prices[-1] - self._lowest_low_array[-1]) /
                (self._highest_high_array[-1] - self._lowest_low_array[-1])
                * 100)

    def get_result(self):
        try:
            result_array = []
            for num in range(-3, 0, 1):
                if self._stoch_osc_array[num] > 80:
                    result_array.append(Option.SELL)
                elif self._stoch_osc_array[num] < 20:
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