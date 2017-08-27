import time
from iqoption import iqapi
from constants import constants
from methods import percentage_change
from databases import LogHandler


class PatternRecognition:
    def __init__(self, array_data_tuple):
        """
        This initialises all the data that is needed in this class
        :param array_data_tuple: 
        """
        # Creates an instance of the iq options api class of this project
        self.api = iqapi.IQOptionApi()

        # This is the array that has the historic data patterns that end up buying
        self._buy_pattern_array = array_data_tuple[0]
        # This is the buy performance array which is the pattern's outcome (same index as pattern)
        self._buy_performance_array = array_data_tuple[1]
        # This is the array that has the historic data patterns that end up selling
        self._sell_pattern_array = array_data_tuple[2]
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._sell_performance_array = array_data_tuple[3]
        # Creates an empty global array for the current pattern
        self._current_pattern = []
        # Creates a ray pattern that fills up just with data so it can be used again and under the length limit
        self.current_raw_pattern = []
        # This will be the number of trades this program does (not what IQOptions will record necessarily)
        self._num_bets = 0
        # Instance of Log handler
        self._log_handler = LogHandler()

    def analyse_pattern(self, data_array, performance_array):
        """
        This function goes through all the data in the arrays and returns the amount of similar patterns
        :param data_array: This is the array that has all the historic data either resulting in a buy or sell
        :param performance_array: This is the equivalent performance array (outcome)
        :return: returns the predicted outcomes array which holds all the outcomes from the similar patterns
        """
        # This is the array of predicted outcomes from all the patterns
        _predicted_outcomes_array = []
        # iterates through the historic data array to find similar patterns
        for b in range(len(data_array)):
            # Uses a should skip boolean to check whether to skip the current pattern completely
            _should_skip = False
            # Gets the pattern that it will use
            _each_pattern = data_array[b]
            # Goes through the pattern and sees if each percentage change is within the right limit, else continue
            for i in range(0, constants.length_of_pattern - 1, 1):
                if abs(percentage_change.percent_change(_each_pattern[i], self._current_pattern[i])) > 350:
                    _should_skip = True
                    break
            # Only skips if one of the data points is too far out and doesn't meet the requirement
            if _should_skip:
                continue
            # If it all passes, then it appends the result of that array to the array that holds all the results
            _predicted_outcomes_array.append(performance_array[b])
        # returns that array
        return _predicted_outcomes_array

    def recognition(self):
        """
        This runs the recognition process on the current pattern
        :return: null
        """
        # This creates a start time to calculate how long it took to run recognition
        _start_time = time.time()
        # Decides whether the pattern is one that starts by going up or down (same as the data arrays from the db)
        if self._current_pattern[1] >= self._current_pattern[0]:
            # It will therefore run the percentage change using the right arrays ie. BUY
            _predicted_outcomes_array = self.analyse_pattern(self._buy_pattern_array, self._buy_performance_array)
        else:
            # It will therefore run the percentage change using the right arrays ie. SELL
            _predicted_outcomes_array = self.analyse_pattern(self._sell_pattern_array, self._sell_performance_array)

        # Calculates the number of patterns found from the returned array of previous outcomes
        _num_patterns_found = len(_predicted_outcomes_array)
        # If the number is greater than the required amount, it can continue
        if _num_patterns_found > constants.patternNumberReq:
            # It averages the outcome of all the numbers in the array to get an average outcome
            _predicted_avg_outcome = sum(_predicted_outcomes_array) / len(_predicted_outcomes_array)

            # It then decides whether the 'difference' is great enough to be worthy of a trade
            # Initialises the _optin to N/A in case that there is not the requierd difference, it won't cause an error
            _option = "N/A"
            if _predicted_avg_outcome < -constants.required_difference:
                # It calls the api to sell
                self.api.buy()
                _option = "SELL"
            elif _predicted_avg_outcome > constants.required_difference:
                # Calls the api to buy
                self.api.sell()
                _option = "BUY"

            # If there has been a trade
            if _option != "N/A":
                # Increase the number of bets that have happened
                self._num_bets += 1
                _sell_array = list(filter(lambda x: x < 0, _predicted_outcomes_array))
                # _sell_array_avg = reduce(lambda x, y: x + y, _sell_array) / len(_sell_array)
                _buy_array = list(filter(lambda x: x > 0, _predicted_outcomes_array))
                _buy_array_avg = reduce(lambda x, y: x + y, _buy_array) / len(_buy_array)
                # Insert into the database all the details for the trade
                self._log_handler.insert(num_patterns=_num_patterns_found,
                                         avg_predicted_outcome=_predicted_avg_outcome,
                                         time_for_recog=time.time() - _start_time,
                                         num_bets=self._num_bets,
                                         num_down_arrays=len(_sell_array),
                                         num_up_arrays=len(_buy_array))

                # Print all the details so it can be seen on the terminal
                print('\n#####\nPatterns Found: {}\nOption: {}\nAvgOutcome: {}\nTime for Recog: {}\nNumber Of Bets: '
                      '{}\nDownArrays {}\nUpArrays {}'.format(_num_patterns_found, _option, _predicted_avg_outcome,
                                                              time.time() - _start_time, self._num_bets,
                                                              len(_sell_array), len(_buy_array)))
            else:
                # No patterns have been found or criteria not met
                self.no_patterns(time.time() - _start_time)

        else:
            # No patterns have been found or criteria not met
            self.no_patterns(time.time() - _start_time)

    def no_patterns(self, final_time):
        """
        This is called when no patterns have been found or the criteria hasn't been  met so a standard input is
        sent to the log_handler class to insert into the database
        :param final_time: this is the time pattern recognition finished in (could be skewed if finishes early)
        :return: null
        """
        # Prints that there are no patterns and inserts the data into the db
        print 'No patterns in: '.format(final_time)
        self._log_handler.insert(num_patterns=None,
                                 avg_predicted_outcome=None,
                                 time_for_recog=final_time,
                                 num_bets=None,
                                 num_down_arrays=None,
                                 num_up_arrays=None)

    def add_to_pattern(self, _next_point):
        """
        This function adds data to the current pattern and also calculates the percentage change within the
        array every time new data is added
        :param _next_point: the data point to be added from the live api
        :return: null
        """
        # TODO: THIS DOESN'T HAVE TO GO THROUGH ALL THE DATA EVERY TIME, JUST THE LAST POINT
        self.current_raw_pattern.append(_next_point)
        temp_pat = []
        if len(self.current_raw_pattern) >= constants.length_of_pattern:
            for i in range(1, len(self.current_raw_pattern), 1):
                temp_pat.append(percentage_change.percent_change(
                    self.current_raw_pattern[0], self.current_raw_pattern[i]))
            self.current_raw_pattern = self.current_raw_pattern[-constants.length_of_pattern:]
            self._current_pattern = temp_pat[-constants.length_of_pattern:]

    def start(self):
        """
        This starts the pattern recognition by syncing with the server time and then
        running the recognition every minute from then on in order to trade
        :return:
        """
        # This syncs the algorithm with the server time so it can use time.sleep later to not use any CPU
        while self.api.get_seconds_left() != 0:
            # Prints the server time left
            print 'Sevrer Time: ', self.api.get_seconds_left()
            # This sleeps for 0.9 seconds seconds so that it only iterates again nearer the correct time
            time.sleep(0.9)
        # Adds the newest data point got from the iqoption api to the pattern for recognition
        try:
            self.add_to_pattern(self.api.get_next_data_point())
        except Exception as e:
            print e



        # Prints the length of the pattern so you know where it is up to
        print 'length of the pattern: ', len(self._current_pattern)
        # Sleeps so that it only runs when the minute is nearly up
        time.sleep(58)
        # Create an infinite loop so that it continues trading until you manually stop it
        first_time_period = time.time()
        second_time_period = first_time_period + (2 * 60 * 60)
        third_time_period = second_time_period + (2 * 60 * 60)
        fourth_time_period = second_time_period + (2 * 60 * 60)
        while time.time():
            # try and catch so that it doesn't break when an error happens because it is on the server
            try:
                # Gets the seconds left. If not 0 then it loops back again and tests again until it is
                if self.api.get_seconds_left() == 0:
                    # Adds it to the current pattern so that it increases in size until length_of_pattern
                    self.add_to_pattern(self.api.get_next_data_point())
                    # Prints the length of the pattern so you know where it is up to
                    print 'length of the pattern: ', len(self._current_pattern)
                    # Only runs recognition if the pattern length is long enough. This is just a test to avoid errors
                    if len(self._current_pattern) >= constants.length_of_pattern:
                        # Run recognition on the current pattern
                        self.recognition()
                    # Sleep for nearly a minute to not waste CPU time
                    time.sleep(58)
            # This is the exception if there are any errors, it will print them
            except Exception as e:
                print e

    # This is put in to avoid errors but I don't know why it is needed so leave it in
    if __name__ == '__main__':
        print 'this has been called by the __main__ thing which is bad'
