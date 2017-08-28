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

    def __init__(self, constants_class):
        """
        Initialises the classes. Starting with loading the data then running iqoption
        then it starts the recognition process
        """
        self.constants = constants


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
        # Starts the recognition part of the program
        return self.start_pattern_recognition(_data_array_tuple, _patterns_array_tuple)

    def start_db(self):
        """
        This starts all the database connections and sets up the handler for the 2 tables
        :return: Array of all data that will be passed into the dataloader class
        """
        # Creates an instance of the database
        self._database = databases.database.Database()
        # Creates an instance of the log handler class
        # self._log_handler = databases.log_handler.LogHandler()
        # Creates an instance of the histdata handler
        self._histdata_handler = databases.histdata_handler.HistDBHandler()
        # Calls the create database function which in turn makes the tables too
        self._database.create_database()
        # Return the full data array
        return self._histdata_handler.get_all_data(), self._histdata_handler.get_all_pattern_data(amount=5000)

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

    def start_pattern_recognition(self, _data_array_tuple, _patterns_array_tuple):
        """
        Starts the recognition with the tuple of data and performance arrays
        :param _patterns_array_tuple:
        :param _data_array_tuple: the tuple of buy and sell data and performance arrays
        :return:
        """
        # Creates recognition class instance
        self._recognition = patternrecognition.recognition.PatternRecognition(
                                            _data_array_tuple, _patterns_array_tuple, self.constants)
        # Starts the recognition on the pattern and the live data from the api in the class
        return self._recognition.start()


constants = constants.Constants()
win_percentages = []
lose_percentages = []
draws_percentages = []

best_win_percentage = 0
best_len_pattern = 0
best_req_patterns = 0
best_req_difference = 0
best_interval = 0

# This alters the pattern length
for i in range(25, 35, 1):
    # This alters the number of required patterns
    for j in range(1000, 5000, 1000):
        # This alters the required difference
        for k in range(70, 80, 5):
            # This alters the intervals of steps when loading data
            for l in range(1, 5, 1):
                constants.set_interval_size(l)
                constants.set_num_pattern_req(j)
                constants.set_pattern_len(i)
                constants.set_required_difference(float(float(k) / float(1000000)))
                # Starts recognition with these settings
                main_class = main(constants)
                result = main_class.start()
                if result[0] > best_win_percentage:
                    best_win_percentage = result[0]
                    best_len_pattern = i
                    best_req_patterns = j
                    best_req_difference = k
                    best_interval = l
                win_percentages.append(result[0])
                lose_percentages.append(result[1])
                draws_percentages.append(result[2])

f = open(os.getcwd() + '/README.md', 'a')
string = 'Max win Percentage: {}\n' \
         'Best Pattern Length: {}\n' \
         'Best Req Num Patterns: {}\n' \
         'Best Req Difference: {}\n' \
         'Best Interval: {}'.format(max(win_percentages),
                                    best_len_pattern,
                                    best_req_patterns,
                                    best_req_difference,
                                    best_interval)
f.write(string)
print string
