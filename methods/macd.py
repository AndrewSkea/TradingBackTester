from enums.enums import Position, Trend, Option
from methods import ema
import functools


class MACD:

    def __init__(self, all_close_data, constants):
        self._all_data = all_close_data
        self.constants = constants
        self._macd_array = []
        self._signal_array = []
        self._multiplier = float(2) / float((self.constants.get_signal_period() + 1))
        self._ema_a = ema.EMA(self._all_data, self.constants.get_ema_a_period())
        self._ema_b = ema.EMA(self._all_data, self.constants.get_ema_b_period())
        self._crossover_array = []
        self._is_new_value = False
        self._position = Position.EQUAL
        self._last_position = Position.EQUAL

    def calculate_initial_macd_array(self):
        """
        Calculates the ema pattern of past data
        :return:
        """
        # Get ema arrays of ema trends
        self._ema_a.calculate_initial_ema_array()
        self._ema_b.calculate_initial_ema_array()
        ema_a_array = self._ema_a.get_ema_array()
        ema_b_array = self._ema_b.get_ema_array()

        # Making the two arrays the same length in order to stop errors
        ema_a_array = ema_a_array[-len(ema_b_array):]
        # Make sure they are the same length here to avoid any errors
#        assert len(ema_b_array) == len(ema_a_array)
        # Go through the list and append the difference between the two ema arrays by index
        for i in range(len(ema_a_array)):
            self._macd_array.append(float(float(ema_b_array[i]) - float(ema_a_array[i])))

    def calculate_initial_signal_array(self):
        # Get the constant for the period of the signal line
        period = self.constants.get_signal_period()
        # Append the average of the first [period] data points to initialise the array
        self._signal_array.append(functools.reduce(lambda x, y: x + y, self._macd_array[:period]) / period)
        for i in range(period, len(self._macd_array[period:]), 1):
            current_signal = (self._macd_array[i] * self._multiplier + self._signal_array[-1] * (1 - self._multiplier))
            self._signal_array.append(current_signal)

    def add_data_point(self, close_value):
        self._is_new_value = False
        ema_a_last_value = self._ema_a.add_data_point(close_value)
        ema_b_last_value = self._ema_b.add_data_point(close_value)
        macd_last_value = ema_b_last_value - ema_a_last_value
        self._macd_array.append(macd_last_value)
        # Get the second last value as last value has just been appended to the macd array. calculate the signal line
        self._signal_array.append(macd_last_value * self._multiplier + self._signal_array[-1] * (1 - self._multiplier))
        self.check_crossover()

    def check_crossover(self):
        try:
            if self._macd_array[-1] > self._signal_array[-1]:
                self._position = Position.ABOVE
            elif self._macd_array[-1] < self._signal_array[-1]:
                self._position = Position.BELOW
            else:
                self._position = Position.EQUAL

                self._last_position = self._crossover_array[-1]
            if self._last_position != self._position:
                if self._last_position == Position.ABOVE:
                    self._crossover_array.append(Trend.DOWN)
                else:
                    self._crossover_array.append(Trend.UP)
                self._last_position = self._position
                self._is_new_value = True
        except Exception as e:
            print('No crossovers so ', e)

    def calculate_initial_crossover_array(self):
        _macd_array = self._macd_array[-len(self._signal_array):]
        # Getting the starting position of the MACD compared to the signal line
        self._position = Position.EQUAL
        if _macd_array[0] > self._signal_array[0]:
            self._position = Position.ABOVE
        elif _macd_array[0] < self._signal_array[0]:
            self._position = Position.BELOW
        self._last_position = self._position

        for i in range(len(_macd_array)):
            if _macd_array[i] > self._signal_array[i]:
                self._position = Position.ABOVE
            elif _macd_array[i] < self._signal_array[i]:
                self._position = Position.BELOW
            else:
                self._position = Position.EQUAL

            if self._last_position != self._position:
                if self._last_position == Position.ABOVE:
                    self._crossover_array.append(Trend.DOWN)
                else:
                    self._crossover_array.append(Trend.UP)
            self._last_position = self._position
            self._is_new_value = True

    def get_result(self):
        """
        This function returns a value if there has been a crossover
        :return: None if no crossover, else direction of crossover
        """
        # If there is a new value on the array
        if self._is_new_value:
            self._is_new_value = False
            if self._crossover_array[-1] == Trend.UP and self._macd_array[-1] > self._macd_array[-2] > self._macd_array[-3]:
                option = Option.BUY
            elif self._crossover_array[-1] == Trend.DOWN and self._macd_array[-1] < self._macd_array[-2] < self._macd_array[-3]:
                option = Option.SELL
            else:
                option = Option.NO_TRADE
            return option
        else:
            self._is_new_value = False
            return None







