import cProfile
import databases
import loaddata
from constants import constants
from patternrecognition import recognition
from methods import macd
from methods import cci
from methods import bollingerbands
from methods import stochastic_oscillator
from methods import rsi
from methods import custom_one, awesome_oscillator
import numpy as np
import pstats
from multiprocessing import Pool

from iqoptionapi.api import IQOptionAPI
import time


class Main(object):
    """
    Where the main thread of execution begins
    Initialises the other classes and starts the recognition
    """

    def __init__(self, constants_class):
        """
        Initialises the classes. Starting with loading the data then running iqoption
        then it starts the recognition process
        """
        self.constants = constants_class

    def start(self):
        """
        The function starts off all the different branches of the program: db set up, loading data, recognition
        :return: null
        """
        # Starts db instance
        # _past_data = self.start_db()
        # Starts the loading of data from the db and passes it into the recognition class
        # pattern_array, performance_array, time_ar, open_price, high_price, low_price, close_price = self.start_loading_data(
        #      all_data_array=_past_data[0])
        pattern_array, performance_array, time_ar, open_price, high_price, low_price, close_price, _patterns_array_tuple = [], [], [], [], [], [], [], []
        # this is the tuple of the arrays of the patterns we will consider 'live' patterns
        # _patterns_array_tuple = self.start_loading_data(all_data_array=_past_data[1])
        # Starts the recognition part of the program
        return self.start_pattern_recognition(pattern_array, performance_array, time_ar, open_price, high_price,
                                              low_price, close_price, _patterns_array_tuple)

    # def start_db(self):
    #     """
    #     This starts all the database connections and sets up the handler for the 2 tables
    #     :return: Array of all data that will be passed into the dataloader class
    #     """
    #     # Creates an instance of the database
    #     _database = databases.database.Database()
    #     # Creates an instance of the log handler class
    #     # self._log_handler = databases.log_handler.LogHandler()
    #     # Creates an instance of the histdata handler
    #     _histdata_handler = databases.histdata_handler.HistDBHandler(self.constants)
    #     # Calls the create database function which in turn makes the tables too
    #     _database.create_database()
    #     # Return the full data array
    #     return _histdata_handler.get_all_pattern_data()
    #
    # def start_loading_data(self, all_data_array):
    #     """
    #     This starts the loading data class which will process the data
    #     :param all_data_array:
    #     :return: the tuple of all the data and performance arrays that will be used by recognition
    #     """
    #     # Sets an instance of the data loader that gets all the percentage change arrays
    #     _loader = loaddata.loader.Loader(all_data_array, self.constants)
    #     return _loader.pattern_storage()

    def start_pattern_recognition(self, pattern_array, performance_array, time_ar, open_price, high_price, low_price,
                                  close_price, _patterns_array_tuple):
        """
        Starts the recognition with the tuple of data and performance arrays
        :param _patterns_array_tuple:
        :param _data_array_tuple: the tuple of buy and sell data and performance arrays
        :return:
        """
        # Sets up the past data for the MACD and Ema
        macd_class = macd.MACD([], self.constants)
        # This creates the CCI class instance and starts all the initial calculations
        cci_class = cci.CCI([], [], [], self.constants)
        # This is creating the Bollinger Band class instance and calculating the initial arrays
        bband_class = bollingerbands.BollingerBands(high_prices=[], low_prices=[],
                                                    close_prices=[], constants_class=self.constants)
        # This is creating the Stochastic Oscillator Class
        stoch_osc = stochastic_oscillator.StochasticOscillator(high_price=[], low_price=[],
                                                               close_price=[],
                                                               constant_class=self.constants)
        # This creates the class for the RSI
        rsi_class = rsi.RSI(close_prices=[], constant_class=self.constants)
        # This is the class for Custom One
        custom_one_class = custom_one.CustomOne(self.constants)

        awesome_oscillator_class = awesome_oscillator.AwesomeOscillator(self.constants)

        open_price, high_price, low_price, close_price = np.loadtxt('eurusd.csv', unpack=True, delimiter=',',
                                                                              usecols=(1, 2, 3, 4))

        quarter = len(open_price)/4
        third = len(open_price)/3
        half = len(open_price)/2
        full = len(open_price)
        used = third

        open_price = open_price[-used:]
        high_price = high_price[-used:]
        low_price = low_price[-used:]
        close_price = close_price[-used:]

        # Creates recognition class instance
        _recognition = recognition.PatternRecognition(list(pattern_array),
                                                      list(performance_array),
                                                      list(time_ar), list(open_price),
                                                      list(high_price), list(low_price),
                                                      list(close_price),
                                                      list(_patterns_array_tuple),
                                                      self.constants,
                                                      macd_class,
                                                      cci_class,
                                                      bband_class,
                                                      stoch_osc,
                                                      rsi_class,
                                                      custom_one_class,
                                                      awesome_oscillator_class)
        # Starts the recognition on the pattern and the live data from the api in the class
        return _recognition.start()


constants = constants.Constants()
main_class = Main(constants)
main_class.start()
