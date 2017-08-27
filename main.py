import time
import os
import databases
import loaddata
import constants
import iqoption
import patternrecognition

class main(object):
    """
    Where the main thread of execution begins
    Initialises the other classes and starts the recognition
    """

    def __init__(self):
        """
        Initialises the classes. Starting with loading the data then running iqoption
        then it starts the recognition process
        """
        self._length_of_pattern = 30
        self.start()


    def start(self):
        """
        The function starts off all the different branchs of the program: db set up, loading data, recognition
        :return: null
        """
        # Starts db instance
        _all_data_array = self.start_db()
        # Starts the loading of data from the db and passes it into the recognition class
        _data_array_tuple = self.start_loading_data(all_data_array=_all_data_array)
        # Starts the recognition part of the program
        self.start_pattern_recognition(_data_array_tuple)
        
    def start_db(self):
        """
        This starts all the database connections and sets up the handler for the 2 tables
        :return: Array of all data that will be passed into the dataloader class
        """
        # Creates an instance of the database
        self._database = databases.database.Database()
        # Creates an instance of the log handler class
        self._log_handler = databases.log_handler.LogHandler()
        # Creates an instance of the histdata handler
        self._histdata_handler = databases.histdata_handler.HistDBHandler()
        # Calls the create database function which in turn makes the tables too
        self._database.create_database()
        # Return the full data array
        return self._histdata_handler.get_all_data()


    def start_loading_data(self, all_data_array):
        """
        This starts the loading data class which will process the data
        :param all_data_array: 
        :return: the tuple of all the data and performance arrays that will be used by recognition
        """
        # Sets an instance of the data loader that
        self._loader = loaddata.loader.Loader(all_data_array)
        # Return the tuple of the 4 arrays
        return self._loader.pattern_storage()

    def start_pattern_recognition(self, _data_array_tuple):
        """
        Starts the recognition with the tuple of data and performance arrays
        :param _data_array_tuple: the tuple of buy and sell data and performance arrays
        :return:
        """
        # Creates recognition class instance
        self._recognition = patternrecognition.recognition.PatternRecognition(_data_array_tuple)
        # Starts the recognition on the pattern and the live data from the api in the class
        self._recognition.start()

main()

