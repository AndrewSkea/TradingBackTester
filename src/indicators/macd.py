# from ..enums.enums import Position, Trend, Option
# from . import ema
#
#
# class MACD:
#
#     def __init__(self, constants):
#         self._all_data = []
#         self.constants = constants
#         self._macd_array = []
#         self._signal_array = []
#         self._multiplier = float(2) / float((self.constants.get_signal_period() + 1))
#         self._ema_a = ema.EMA(self.constants.get_ema_a_period())
#         self._ema_b = ema.EMA(self.constants.get_ema_b_period())
#         self._crossover_array = []
#         self._is_new_value = False
#         self._position = Position.EQUAL
#         self._last_position = Position.EQUAL
#
#     def add_data_point(self, close_value):
#         try:
#             self._is_new_value = False
#             ema_a_last_value = self._ema_a.update_data_arrays(close_value)
#             ema_b_last_value = self._ema_b.update_data_arrays(close_value)
#             macd_last_value = ema_b_last_value - ema_a_last_value
#             self._macd_array.append(macd_last_value)
#             # Get the second last value as last value has just been appended to the macd array. calculate the signal line
#             if len(self._signal_array) > 1:
#                 self._signal_array.append(macd_last_value * self._multiplier + self._signal_array[-1] * (1 - self._multiplier))
#             else:
#                 self._signal_array.append(macd_last_value)
#             self.check_crossover()
#         except TypeError as e:
#             pass#print("Possibly an error when ema_a - ema_b happens, if so skip this add", e)
#
#     def check_crossover(self):
#         try:
#             if self._macd_array[-1] > self._signal_array[-1]:
#                 self._position = Position.ABOVE
#             elif self._macd_array[-1] < self._signal_array[-1]:
#                 self._position = Position.BELOW
#             else:
#                 self._position = Position.EQUAL
#
#                 self._last_position = self._crossover_array[-1]
#             if self._last_position != self._position:
#                 if self._last_position == Position.ABOVE:
#                     self._crossover_array.append(Trend.DOWN)
#                 else:
#                     self._crossover_array.append(Trend.UP)
#                 self._last_position = self._position
#                 self._is_new_value = True
#         except Exception:
#             pass
#
#     def get_result(self):
#         """
#         This function returns a value if there has been a crossover
#         :return: None if no crossover, else direction of crossover
#         """
#         # If there is a new value on the array
#         try:
#             if self._is_new_value:
#                 self._is_new_value = False
#                 if self._crossover_array[-1] == Trend.UP and self._macd_array[-1] > self._macd_array[-2]:
#                     option = Option.BUY
#                 elif self._crossover_array[-1] == Trend.DOWN and self._macd_array[-1] < self._macd_array[-2]:
#                     option = Option.SELL
#                 else:
#                     option = Option.NO_TRADE
#                 return option
#             else:
#                 self._is_new_value = False
#                 return Option.NO_TRADE
#         except IndexError:
#             return Option.NO_TRADE
#
#     def get_result_for_nn(self):
#         return self.get_result().value
#
#
#
#
#
#
#
