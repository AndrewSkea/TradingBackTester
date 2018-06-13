import random
import time
import logging

import pandas as pd

from .indicators.data_arrays import DataArrays
from .backtest import backtest


class Main(object):
    def __init__(self):
        self._data_class = DataArrays(period=20)
        data_arrays = pd.read_csv('src/data/eurusd_m1.csv', engine='python')
        date_ar, self.time_ar, self.open_ar, self.high_ar, self.low_ar, self.close_ar = zip(*data_arrays.as_matrix())
        self.date_time_ar = [time.strptime("{} {}".format(date_ar[i], self.time_ar[i]), "%m/%d/%Y %H:%M:%S")
                             for i in range(len(date_ar))]

    def start(self, json_config=None):
        if json_config is None:
            logging.warning("Need JSON str or Dict parameter for method configuration, pulling from file")
            with open('src/data/config.json', 'r') as file:
                json_config = file.read()
        time_frame = json_config['timeframe']
        num_trades = 0
        split = len(self.date_time_ar)
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
        if json_config['is_random']:
            rand_int = random.randint(0, len(self.open_ar) - split)
            _back_test = backtest.PatternRecognition(self._data_class,
                                                     list(self.date_time_ar[rand_int:rand_int + split]),
                                                     list(self.open_ar[rand_int:rand_int + split]),
                                                     list(self.high_ar[rand_int:rand_int + split]),
                                                     list(self.low_ar[rand_int:rand_int + split]),
                                                     list(self.close_ar[rand_int:rand_int + split]),
                                                     json_config)
        else:
            _back_test = backtest.PatternRecognition(self._data_class,
                                                     list(self.date_time_ar[-split:]),
                                                     list(self.open_ar[-split:]),
                                                     list(self.high_ar[-split:]),
                                                     list(self.low_ar[-split:]),
                                                     list(self.close_ar[-split:]),
                                                     json_config)
        return _back_test.start(num_trades)
