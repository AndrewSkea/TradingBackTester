import os
import time
from data.data_arrays import DataArrays
from constants import constants
from patternrecognition import recognition
import pandas as pd


class Main(object):
    """
    Where the main thread of execution begins
    Initialises the other classes and starts the recognition
    """

    def __init__(self):
        self.constants = constants.Constants()
        self._data_class = DataArrays(period=20)
        # self.api = iqapi.IQOptionApi()

    def start(self):
        # start_time = time.time()
        # time_ar, open_ar, high_ar, low_ar, close_ar = self.api.get_starting_data_points()
        data_arrays = pd.read_csv('databases/eurusd_m1.csv', engine='python')
        date_ar, time_ar, open_ar, high_ar, low_ar, close_ar = zip(*data_arrays.as_matrix())
        date_time_ar = [time.strptime("{} {}".format(date_ar[i], time_ar[i]), "%m/%d/%Y %H:%M:%S")
                        for i in range(len(date_ar))]
        # per = 1
        # split = int(len(open_price) / per)
        # time_ar = time_ar[-split:]
        # open_price = open_price[-split:]
        # high_price = high_price[-split:]
        # low_price = low_price[-split:]
        # close_price = close_price[-split:]
        assert len(date_time_ar) == len(open_ar) == len(high_ar) == len(low_ar) == len(close_ar)
        # print("Loaded in {}s Using 1/{} of the data-set.\nWe want {} trades (5 trades a day) at 65% win rate"
        #       .format(int(round(time.time() - start_time, 1)), per, int(5 * 365 / per)))

        # with open('data/fxcm_data_5_mins.csv', 'a') as file:
        #     for i in range(len(time_ar)):
        #         tmp_str = "{},{},{},{},{}\n".format(time_ar[i], open_ar[i], high_ar[i], low_ar[i], close_ar[i])
        #         file.write(tmp_str)
        # print("Time taken: ", time.time() - start_time)
        time_frame = os.environ.get('TIMEFRAME')
        split = len(date_time_ar)
        if time_frame == 'day':
            split = 1440
        elif time_frame == 'week':
            split = 10080
        elif time_frame == 'month':
            split = 40320
        elif time_frame == '3_months':
            split = 124992
        elif time_frame == 'half_year' or time_frame == '6_months':
            split = 262800
        elif time_frame == 'year':
            split = 525600
        _recognition = recognition.PatternRecognition(self._data_class,
                                                      list(date_time_ar[-split:]),
                                                      list(open_ar[-split:]),
                                                      list(high_ar[-split:]),
                                                      list(low_ar[-split:]),
                                                      list(close_ar[-split:]))
        # Starts the recognition on the pattern and the live data from the api in the class
        return _recognition.start()


main_class = Main()
main_class.start()
