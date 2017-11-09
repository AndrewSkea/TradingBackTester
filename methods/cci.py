from methods.typical_price import TypicalPrice
from enums.enums import Option, Trend
import time

def percent_change(_start_point, _current_point):
    try:
        if _start_point > _current_point:
            x = -((float(_start_point) - float(_current_point)) / abs(_current_point)) * 100
        else:
            x = ((float(_current_point) - float(_start_point)) / abs(_start_point)) * 100
        if x == 0.0:
            return 0.000000001
        else:
            return x
    except:
        return 0.000000001


class CCI:
    """
    This is the CCI class that takes calculates, and provides CCI data on the patterns
    """

    def __init__(self, high_price, low_price, close_price, constant_class):
        # This is the CCI array
        self._cci_array = []
        # THis is the constants class
        self._constant_class = constant_class
        # This is the CCI constant (normally 0.015 on the internet)
        self._cci_constant = self._constant_class.get_cci_constant()
        # Get the CCI limit constant
        self._cci_limit = self._constant_class.get_cci_limit()
        # This is the period for the CCI class
        self._cci_period = self._constant_class.get_cci_period()
        # This is the Typical Price array class that this class will use
        self._tp_class = TypicalPrice(high_price, low_price, close_price, self._constant_class)
        # This makes the tp class calculate the initial tp array
        self._tp_class.calculate_initial_array()
        self._tp_array = self._tp_class.get_typical_price_array()
        # This makes the tp class calculate the sma array for the tp
        self._tp_class.calculate_initial_sma_of_tp()
        self._tp_sma_array = self._tp_class.get_sma_array_for_tp()
        # This makes the tp class calculate the standard deviation array for the tp class
        self._tp_class.calculate_initial_md_array()
        self._md_array = self._tp_class.get_standard_deviation_array_for_tp()
        self._trend_index = 0
        # MAKE SURE THIS IS DIVISIBLE BY 4
        self._trend_length = 12
        # Percentage change period
        self._pc_period = 20
        # Percentage change array for CCI
        self._pc_cci = []

    def calculate_cci_initial_array(self):
        """
        This calculates the cci initial array
        :return:
        """
        for i in range(len(self._md_array)):
            try:
                self._cci_array.append((self._tp_array[i + self._cci_period] - self._tp_sma_array[i]) /
                                       (self._cci_constant * self._md_array[i]))
            except IndexError:
                print('Index Error at index: ', i)
        for j in range(len(self._cci_array) - (self._pc_period * 10), len(self._cci_array), self._pc_period):
            try:
                self._pc_cci.append((self._cci_array[j-self._pc_period:j]))
            except IndexError as e:
                print('Index error in pc of cci:, ', e)

    def add_to_cci_array(self, close, high, low):
        tp, sma, dev = self._tp_class.add_last_point(close, high, low)
        self._cci_array.append((tp - sma) /
                               (self._cci_constant * dev))

    def update_arrays(self):
        self._tp_array = self._tp_class.get_typical_price_array()
        self._tp_sma_array = self._tp_class.get_sma_array_for_tp()
        self._md_array = self._tp_class.get_standard_deviation_array_for_tp()

    def get_cci_array_(self):
        return self._cci_array

    def get_result(self):
        result_array = []
        cci_array = self._cci_array[-self._pc_period:]
        res = []
        for pattern in self._pc_cci:
            # num_similar = 0
            # for n in range(len(pattern)):
            #     if pattern[n] - 20 < cci_array[n] < pattern[n] + 20:
            #         num_similar += 1
            num = int(len(pattern) / 2)
            avg_1 = float(sum(pattern[:num])) / float(num)
            avg_4 = float(sum(pattern[num:])) / float(num)

            if avg_1 < avg_4:
                res.append(Trend.UP)
            elif avg_4 < avg_1:
                res.append(Trend.DOWN)
            # if num_similar > 10:
            #     result_array.append(pattern)
        if res.count(Trend.UP) > res.count(Trend.DOWN) + 3:
            final_res = Trend.UP
        elif res.count(Trend.DOWN) > res.count(Trend.UP) + 3:
            final_res = Trend.DOWN
        else:
            final_res = Trend.STRAIGHT

        pat_num = int(len(cci_array) / 2)
        pat_avg_1 = float(sum(cci_array[:pat_num])) / float(pat_num)
        pat_avg_4 = float(sum(cci_array[pat_num:])) / float(pat_num)

        if pat_avg_1 < pat_avg_4 and final_res == Trend.UP:
            return Option.BUY, 0
        elif pat_avg_4 < pat_avg_1 and final_res == Trend.DOWN:
            return Option.SELL, 0
        else:
            return Option.NO_TRADE, 0

        # option = Option.NO_TRADE
        # trend = []
        # final_trend = Trend.STRAIGHT
        # print(len(result_array))
        # if len(result_array) >= 1:
        #     for pat in result_array:
        #         num = int(len(pat) / 2)
        #         avg_1 = float(sum(pat[:num])) / float(num)
        #         avg_4 = float(sum(pat[num:])) / float(num)
        #         print(avg_1, '  :  ', avg_4)
        #         if avg_4 > avg_1:
        #             trend.append(Trend.UP)
        #             print('UP')
        #         elif avg_4 < avg_1:
        #             trend.append(Trend.DOWN)
        #             print('DOWN')
        #     if trend.count(Trend.UP) > trend.count(Trend.DOWN):
        #         final_trend = Trend.UP
        #     elif trend.count(Trend.UP) < trend.count(Trend.DOWN):
        #         final_trend = Trend.DOWN
        #     if final_trend == Trend.UP:             # int(self._cci_array[-1]) > -20 and
        #         option = Option.BUY
        #     elif final_trend == Trend.DOWN:         # int(self._cci_array[-1]) < 20 and
        #         option = Option.SELL
        # return option, 0

    def get_amount_of_consecutive_times_cci_is_over_traded(self):
        """
        This returns the amount times the cci has been over-traded. So, if the last few values have been under -100 or
        above 100, it counts the amount of times, this has happened and returns the value
        :return: The number of consecutive times the cci has been over traded
        """
        if self._cci_array[-1] < -100:
            for i in range(len(self._cci_array)):
                if self._cci_array[-i] < -100:
                    continue
                else:
                    return i
        elif self._cci_array[-1] > 100:
            for i in range(len(self._cci_array)):
                if self._cci_array[-i] > 100:
                    continue
                else:
                    return i
        else:
            return 0
