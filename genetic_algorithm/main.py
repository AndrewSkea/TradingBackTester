from constants import Constants
from random import randint, uniform
import cProfile
import databases
import loaddata
import constants
import patternrecognition
from methods import macd
from methods import cci
from methods import bollingerbands
from multiprocessing import Pool
import dill

class GeneticAlgorithm:

    def __init__(self):
        # This is the array of agents in the population (starting with a population of around 20)
        self._agent_array = []
        # This is the target result for the genetic algorithm to try and work towards
        self._target_result = 0.80
        # Number of agents
        self._num_agents = 20
        # This is the top percentage you take to the next round
        self._top_percentage = int(0.6 * self._num_agents)
        # This is the best score tuple with the agent and its score
        self._best_score_agent = (None, 0)
        # This is the process pool
        self._pool = Pool(processes=4)

    def create_agents(self):
        for i in range(self._num_agents):
            self._agent_array.append(GeneticMain(self.create_random_constants_class()))

    def crossover(self, agent1, agent2):
        crossover_index = randint(1, 11)
        constants_state_1 = agent1.get_constants_class_instance().get_genetic_algorithm_list_state()
        constants_state_2 = agent2.get_constants_class_instance().get_genetic_algorithm_list_state()

        start_crossover_list_1 = constants_state_1[:crossover_index]
        end_constants_state_1 = constants_state_1[crossover_index:]

        start_crossover_list_2 = constants_state_2[:crossover_index]
        end_constants_state_2 = constants_state_2[crossover_index:]

        final_list_1 = start_crossover_list_2
        final_list_1.append(end_constants_state_1)
        final_list_2 = start_crossover_list_1
        final_list_2.append(end_constants_state_2)

        agent1.reset_constants_class(final_list_1)
        agent2.reset_constants_class(final_list_2)

        return agent1, agent2

    def mutate(self):
        pass

    def start(self):
        self.create_agents()
        index = 0
        while self._best_score_agent[1] < self._target_result or index < 10:
            result_array = self._pool.map(self.start_agent, zip([self]*len(self._agent_array), self._agent_array))
            final_results_array = []
            for i in range(len(result_array)):
                final_results_array.append(self._agent_array[i], result_array[i])

            # This sorts the group in ascending order with percentage win
            sorted(final_results_array, key=lambda x: x[1])
            # This gets the top percentage of the group and discards the rest of them
            final_results_array = final_results_array[self._top_percentage:]
            self._best_score_agent = final_results_array[-1]

            self._agent_array = []

            while len(final_results_array) != 0:
                if len(final_results_array) >= 2:
                    first_chosen_index = randint(0, len(final_results_array))
                    first_chosen = final_results_array[first_chosen_index][0]
                    del final_results_array[first_chosen_index]
                    second_chosen_index = randint(0, len(final_results_array))
                    second_chosen = final_results_array[first_chosen_index][0]
                    del final_results_array[second_chosen_index]

                    child1, child2 = self.crossover(first_chosen, second_chosen)

                    self._agent_array.append(child1)
                    self._agent_array.append(child2)
                else:
                    del final_results_array[0]

            index += 1

        best_agent = self._best_score_agent[0]
        constants_class = best_agent.get_constants_class_instance()
        constants_state_table = constants_class.get_str_table()
        print constants_state_table

        _file = open("logdata/constants_log.txt", 'a')
        _file.write(constants_state_table)
        _file.write("\n")
        _file.close()

    def start_agent(self, agent_class):
        agent_class.start()

    def create_random_constants_class(self):
        """
        Creates an instance of a constants class with random variables assigned
        :return: return the instance
        """
        constants_class = Constants()
        constants_class.set_pattern_len(randint(20, 50))
        constants_class.set_num_pattern_req(randint(2000, 10000))
        constants_class.set_required_difference(uniform(0.001, 0.0001))
        constants_class.set_interval_size(randint(1, 20))
        i = randint(10, 100)
        constants_class.set_ema_a_period(i)
        constants_class.set_ema_b_period(randint(i, i + 100))
        constants_class.set_signal_period(randint(5, i))
        constants_class.set_cci_period(randint(10, 50))
        constants_class.set_cci_constant(0.015)
        constants_class.set_typical_price_ema_period(randint(10, 100))
        constants_class.set_bollinger_band_sma_period(randint(10, 100))
        constants_class.set_cci_limit(randint(100, 300))
        return constants_class


class GeneticMain(object):
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

    def get_constants_class_instance(self):
        """
        This returns the instance of the constants class that has been used
        :return: The constants class
        """
        return self.constants

    def reset_constants_class(self, lst):
        """
        Creates an instance of a constants class with random variables assigned
        :return: return the instance
        """
        self.constants.set_pattern_len(lst[0])
        self.constants.set_num_pattern_req(lst[1])
        self.constants.set_required_difference(lst[2])
        self.constants.set_interval_size(lst[3])
        self.constants.set_ema_a_period(lst[4])
        self.constants.set_ema_b_period(lst[5])
        self.constants.set_signal_period(lst[6])
        self.constants.set_cci_period(lst[7])
        self.constants.set_cci_constant(lst[8])
        self.constants.set_typical_price_ema_period(lst[9])
        self.constants.set_bollinger_band_sma_period(lst[10])
        self.constants.set_cci_limit(lst[11])

    def start(self):
        """
        The function starts off all the different branches of the program: db set up, loading data, recognition
        :return: null
        """
        # Starts db instance
        _past_data = self.start_db()
        # Starts the loading of data from the db and passes it into the recognition class
        pattern_array, performance_array, time_ar, open_price, high_price, low_price, close_price = self.start_loading_data(all_data_array=_past_data[0])
        # this is the tuple of the arrays of the patterns we will consider 'live' patterns
        _patterns_array_tuple = self.start_loading_data(all_data_array=_past_data[1])
        # Starts the recognition part of the program
        return self.start_pattern_recognition(pattern_array, performance_array, time_ar, open_price, high_price, low_price, close_price, _patterns_array_tuple)

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
               _histdata_handler.get_all_pattern_data()

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

    def start_pattern_recognition(self, pattern_array, performance_array, time_ar, open_price, high_price, low_price, close_price, _patterns_array_tuple):
        """
        Starts the recognition with the tuple of data and performance arrays
        :param _patterns_array_tuple:
        :param _data_array_tuple: the tuple of buy and sell data and performance arrays
        :return:
        """
        # Sets up the past data for the MACD and Ema
        macd_class = macd.MACD(close_price, self.constants)
        macd_class.calculate_initial_macd_array()
        macd_class.calculate_initial_signal_array()
        macd_class.calculate_initial_crossover_array()
        # This creates the CCI class instance and starts all the initial calculations
        cci_class = cci.CCI(high_price, low_price, close_price, self.constants)
        cci_class.calculate_cci_initial_array()
        # This is creating the Bollinger Band class instance and calculating the initial arrays
        bband_class = bollingerbands.BollingerBands(close_price, self.constants)
        bband_class.calculate_initial_arrays()

        # Creates recognition class instance
        _recognition = patternrecognition.PatternRecognition(pattern_array,
                                                             performance_array,
                                                             time_ar, open_price,
                                                             high_price, low_price,
                                                             close_price,
                                                             _patterns_array_tuple,
                                                             self.constants,
                                                             macd_class,
                                                             cci_class,
                                                             bband_class)
        # Starts the recognition on the pattern and the live data from the api in the class
        return _recognition.start()


def start_the_genetic_algorithm():
    return GeneticAlgorithm().start()

# This is put in to avoid errors but I don't know why it is needed so leave it in
if __name__ == '__main__':
    start_the_genetic_algorithm()
