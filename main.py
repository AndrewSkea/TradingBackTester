import cProfile
import databases
import loaddata
import constants
import patternrecognition
from methods import macd
from methods import cci
import pstats


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
        _past_data = self.start_db()
        # Starts the loading of data from the db and passes it into the recognition class
        _data_array_tuple = self.start_loading_data(all_data_array=_past_data[0])
        # this is the tuple of the arrays of the patterns we will consider 'live' patterns
        _patterns_array_tuple = self.start_loading_data(all_data_array=_past_data[1])
        # this is the tuple of the arrays of the patterns we will consider for the indicators to work
        _indicator_data_array_tuple = self.start_loading_data(all_data_array=_past_data[2])
        # Starts the recognition part of the program
        return self.start_pattern_recognition(_data_array_tuple, _patterns_array_tuple, _indicator_data_array_tuple)

    def start_db(self):
        """
        This starts all the database connections and sets up the handler for the 2 tables
        :return: Array of all data that will be passed into the dataloader class
        """
        # Creates an instance of the database
        _database = databases.database.Database()
        # Creates an instance of the log handler class
        # self._log_handler = databases.log_handler.LogHandler()
        # Creates an instance of the histdata handler
        _histdata_handler = databases.histdata_handler.HistDBHandler(self.constants)
        # Calls the create database function which in turn makes the tables too
        _database.create_database()
        # Return the full data array
        return _histdata_handler.get_all_data(), \
               _histdata_handler.get_all_pattern_data(), \
               _histdata_handler.get_all_data_for_indicators()

    def start_loading_data(self, all_data_array):
        """
        This starts the loading data class which will process the data
        :param all_data_array: 
        :return: the tuple of all the data and performance arrays that will be used by recognition
        """
        # Sets an instance of the data loader that gets all the percentage change arrays
        _loader = loaddata.loader.Loader(all_data_array, self.constants)
        # Return the tuple of the 4 arrays
        return _loader.pattern_storage()

    def start_pattern_recognition(self, _data_array_tuple, _patterns_array_tuple, _indicator_data_array_tuple):
        """
        Starts the recognition with the tuple of data and performance arrays
        :param _indicator_data_array_tuple:
        :param _patterns_array_tuple:
        :param _data_array_tuple: the tuple of buy and sell data and performance arrays
        :return:
        """
        # Sets up the past data for the MACD and Ema
        macd_class = macd.MACD(_data_array_tuple[6], self.constants)
        macd_class.calculate_initial_macd_array()
        macd_class.calculate_initial_signal_array()
        macd_class.calculate_initial_crossover_array()
        # This creates the CCI class instance and starts all the initial calculations
        cci_class = cci.CCI(_data_array_tuple, self.constants)
        cci_class.calculate_cci_initial_array()

        # Creates recognition class instance
        _recognition = patternrecognition.PatternRecognition(_data_array_tuple,
                                                             _patterns_array_tuple,
                                                             _indicator_data_array_tuple,
                                                             self.constants,
                                                             macd_class,
                                                             cci_class)
        # Starts the recognition on the pattern and the live data from the api in the class
        return _recognition.start()


constants = constants.Constants()
main_class = Main(constants)
main_class.start()

# option = raw_input('Profiler (y/n): ')
# if option == 'n':
#     constants = constants.Constants()
#     main_class = Main(constants)
#     main_class.start()
# else:
#     constants = constants.Constants()
#     main_class = Main(constants)
#     cProfile.run('main_class.start()', 'profiler_stats', 4)
#     p = pstats.Stats('profiler_stats')
#     p.strip_dirs().sort_stats(-1).print_stats()