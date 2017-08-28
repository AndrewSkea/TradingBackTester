class Constants:
    def __init__(self):
        self._length_of_pattern = 25
        self._num_pattern_req = 1000
        self._required_difference = 0
        self._interval_size = 1

    def set_pattern_len(self, num):
        self._length_of_pattern = num

    def set_num_pattern_req(self, num):
        self._num_pattern_req = num

    def set_required_difference(self, num):
        self._required_difference = num

    def set_interval_size(self, num):
        self._interval_size = num

    def get_pattern_len(self):
        return self._length_of_pattern

    def get_num_pattern_req(self):
        return self._num_pattern_req

    def get_required_difference(self):
        return self._required_difference

    def get_interval_size(self):
        return self._interval_size
