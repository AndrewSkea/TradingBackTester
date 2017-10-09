from enums import enums


def percent_change(_start_point, _current_point):
    try:
        if _start_point > _current_point:
            x = -((float(_start_point) - float(_current_point)) / abs(_current_point)) * 100
        else:
            x = ((float(_current_point) - float(_start_point)) / abs(_start_point)) * 100
        if x == 0.0:
            return 0.000000001
        else:
            return x
    except:
        return 0.000000001


class PercentageChange:
    def __init__(self, constants, _pattern_array, _performance_array):
        self.constants = constants
        self._pattern_array = _pattern_array
        self._performance_array = _performance_array

    def get_predicted_outcomes(self, pattern):
        """
        This function goes through all the data in the arrays and returns the amount of similar patterns
        :param pattern:
        :return: returns the predicted outcomes array which holds all the outcomes from the similar patterns
        """
        # This is the array of predicted outcomes from all the patterns
        _predicted_outcomes_array = []
        # iterates through the historic data array to find similar patterns
        for b in range(len(self._pattern_array)):
            # Uses a should skip boolean to check whether to skip the current pattern completely
            _should_skip = False
            # Gets the pattern that it will use
            _each_pattern = self._pattern_array[b]
            # Goes through the pattern and sees if each percentage change is within the right limit, else continue
            for i in range(0, self.constants.get_pattern_len() - 1, 1):
                if abs(percent_change(_each_pattern[i], pattern[i])) > 500:
                    _should_skip = True
                    break
            # Only skips if one of the data points is too far out and doesn't meet the requirement
            if _should_skip:
                continue
            # If it all passes, then it appends the result of that array to the array that holds all the results
            _predicted_outcomes_array.append(self._performance_array[b])
        # returns that array
        return _predicted_outcomes_array

    def get_result_of_pc(self, pattern):
        _predicted_outcomes_array = self.get_predicted_outcomes(pattern)

        # Calculates the number of patterns found from the returned array of previous outcomes
        _num_patterns_found = len(_predicted_outcomes_array)
        # If the number is greater than the required amount, it can continue
        if _num_patterns_found > self.constants.get_num_pattern_req():
            # It averages the outcome of all the numbers in the array to get an average outcome
            _predicted_avg_outcome = reduce(lambda x, y: x + y, _predicted_outcomes_array) / _num_patterns_found

            # It then decides whether the 'difference' is great enough to be worthy of a trade
            # Initialises the _option to N/A in case that there is not the required difference, it won't cause an error
            _option = enums.Option.NO_TRADE
            if _predicted_avg_outcome < -self.constants.get_required_difference():
                # SELLS
                _option = enums.Option.SELL
            elif _predicted_avg_outcome > self.constants.get_required_difference():
                # BUYS
                _option = enums.Option.BUY

            # If there has been a trade
            if _option != enums.Option.NO_TRADE:
                return _option
            else:
                # No patterns have been found or criteria not met
                return None
        else:
            return None
