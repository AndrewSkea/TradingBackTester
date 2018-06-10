import os
import time
import random
from src.data.data_arrays import DataArrays
from src import backtest
import pandas as pd


class Main(object):
    """
    Where the main thread of execution begins
    Initialises the other classes and starts the recognition
    """

    def __init__(self):
        self._data_class = DataArrays(period=20)

    def start(self):
        data_arrays = pd.read_csv('src/data/eurusd_m1_small.csv', engine='python')
        date_ar, time_ar, open_ar, high_ar, low_ar, close_ar = zip(*data_arrays.as_matrix())
        date_time_ar = [time.strptime("{} {}".format(date_ar[i], time_ar[i]), "%m/%d/%Y %H:%M:%S")
                        for i in range(len(date_ar))]
        assert len(date_time_ar) == len(open_ar) == len(high_ar) == len(low_ar) == len(close_ar)
        time_frame = os.environ.get('TIMEFRAME')
        num_trades = 0
        split = len(date_time_ar)
        if time_frame == 'day':
            num_trades = 5
            split = 1440
        elif time_frame == 'week':
            num_trades = 25
            split = 10080
        elif time_frame == 'month':
            num_trades = 120
            split = 40320
        elif time_frame == '3_months':
            num_trades = 300
            split = 124992
        elif time_frame == 'half_year' or time_frame == '6_months':
            num_trades = 650
            split = 262800
        elif time_frame == 'year':
            num_trades = 1500
            split = 525600
        json_config = None
        if os.environ.get('FROM_JSON_FILE'):
            with open('src/data/config.json', 'r') as file:
                json_config = file.read()
        # if os.environ.get('IS_RANDOM'):
        #     rand_int = random.randint(0, len(open_ar) - split)
        #     _backtest = backtest.PatternRecognition(self._data_class,
        #                                             list(date_time_ar[rand_int:rand_int + split]),
        #                                             list(open_ar[rand_int:rand_int + split]),
        #                                             list(high_ar[rand_int:rand_int + split]),
        #                                             list(low_ar[rand_int:rand_int + split]),
        #                                             list(close_ar[rand_int:rand_int + split]),
        #                                             json_config)
        # else:
        _backtest = backtest.PatternRecognition(self._data_class,
                                                list(date_time_ar[-split:]),
                                                list(open_ar[-split:]),
                                                list(high_ar[-split:]),
                                                list(low_ar[-split:]),
                                                list(close_ar[-split:]),
                                                json_config)
        # Starts the recognition on the pattern and the live data from the api in the class
        return _backtest.start(num_trades)


main_class = Main()
main_class.start()
