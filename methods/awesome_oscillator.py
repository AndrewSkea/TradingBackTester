from enums.enums import Position, Trend, Option
from methods import sma


class AwesomeOscillator:
    def __init__(self, constants):
        self._all_data = []
        self.constants = constants
        self._sma_a = sma.SMA(28)
        self._sma_b = sma.SMA(5)
        self._awesome_oscillator = []
        self._crossover_array = []

    def add_data_point(self, close_value, low_value, high_value):
        mid_point = (low_value + high_value) / 2
        point1 = self._sma_a.add_data_point(mid_point)
        point2 = self._sma_b.add_data_point(mid_point)
        self._awesome_oscillator.append(point2 - point1)

    def get_awesome_oscillator_array(self):
        return self._awesome_oscillator

    def get_result(self):
        """
        This function returns a value if there has been a crossover
        :return: None if no crossover, else direction of crossover
        """
        try:
            if self._awesome_oscillator[-1] < 0 < self._awesome_oscillator[-2]:
                return Option.SELL
            elif self._awesome_oscillator[-1] > 0 > self._awesome_oscillator[-2]:
                return Option.BUY
            else:
                return Option.NO_TRADE
        except IndexError:
            return Option.NO_TRADE

    def get_result_for_custom_one(self):
        """
        This function returns a value if there has been a crossover
        :return: None if no crossover, else direction of crossover
        """
        try:
            if self._awesome_oscillator[-1] < 0 < self._awesome_oscillator[-2]:
                self._crossover_array.append(Position.BELOW)
                return Option.SELL
            elif self._awesome_oscillator[-1] > 0 > self._awesome_oscillator[-2]:
                self._crossover_array.append(Position.ABOVE)
                return Option.BUY
            else:
                self._crossover_array.append(Position.EQUAL)
                return Option.NO_TRADE
        except IndexError:
            return Option.NO_TRADE

