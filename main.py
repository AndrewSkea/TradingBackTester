from constants import constants
from patternrecognition import recognition
from methods import macd
from methods import cci
from methods import bollingerbands
from methods import stochastic_oscillator
from methods import rsi
from methods import custom_one, awesome_oscillator, custom_two, custom_three
import numpy as np
from loaddata.loader import Loader
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

        custom_two_class = custom_two.CustomTwo(self.constants)

        custom_three_class = custom_three.CustomThree(self.constants)

        awesome_oscillator_class = awesome_oscillator.AwesomeOscillator(self.constants)

        open_price, high_price, low_price, close_price = np.loadtxt('eurusd.csv', unpack=True, delimiter=',',
                                                                    usecols=(1, 2, 3, 4))

        # loader = Loader()
        # loader.load_data(20)
        # datasets = loader.get_datasets()
        # print(len(datasets))
        # time.sleep(4)

        quarter = len(open_price) / 4
        third = len(open_price) / 3
        half = len(open_price) / 2
        full = len(open_price)
        used = third

        open_price = open_price[-used:]
        high_price = high_price[-used:]
        low_price = low_price[-used:]
        close_price = close_price[-used:]

        # Creates recognition class instance
        _recognition = recognition.PatternRecognition([],
                                                      [],
                                                      [],
                                                      list(open_price),
                                                      list(high_price),
                                                      list(low_price),
                                                      list(close_price),
                                                      [],
                                                      self.constants,
                                                      macd_class,
                                                      cci_class,
                                                      bband_class,
                                                      stoch_osc,
                                                      rsi_class,
                                                      custom_one_class,
                                                      awesome_oscillator_class,
                                                      custom_two_class,
                                                      custom_three_class)
        # Starts the recognition on the pattern and the live data from the api in the class
        return _recognition.start()


constants = constants.Constants()
main_class = Main(constants)
main_class.start()
