import numpy as np
import datetime
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
        """
        Initialises the classes. Starting with loading the data then running iqoption
        then it starts the recognition process
        """
        self.constants = constants.Constants()
        self._data_class = DataArrays(period=20)

    def start(self):
        start_time = time.time()
        data_arrays = pd.read_csv('databases/data.csv',
                                  converters={0: lambda x: time.strptime(str(x), '%Y%m%d-%H%M%S')}, engine='python')
        time_ar, open_price, high_price, low_price, close_price = zip(*data_arrays.as_matrix())
        per = 1
        split = int(len(open_price) / per)
        time_ar = time_ar[-split:]
        open_price = open_price[-split:]
        high_price = high_price[-split:]
        low_price = low_price[-split:]
        close_price = close_price[-split:]
        assert len(time_ar) == len(open_price) == len(high_price) == len(low_price) == len(close_price)
        print("Loaded in {}s Using 1/{} of the data-set.\nWe want {} trades (5 trades a day) at 65% win rate"
              .format(int(round(time.time() - start_time, 1)), per, int(5 * 365 / per)))

        _recognition = recognition.PatternRecognition(self._data_class,
                                                      list(time_ar),
                                                      list(open_price),
                                                      list(high_price),
                                                      list(low_price),
                                                      list(close_price))
        # Starts the recognition on the pattern and the live data from the api in the class
        return _recognition.start()


main_class = Main()
main_class.start()
