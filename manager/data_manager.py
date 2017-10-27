

class DataManager:

    def __init__(self, array_data_tuple):
        # This is the macd array
        self._macd_array = []
        # This is the ema data array
        self._ema_array = []
        # This is the percentage change array
        self._percentage_change_array = []
        # THis is the sma array
        self._sma_array = []
        # This is the mean deviation array
        self._mean_deviation = []
        # This is the CCI array
        self._cci = []
        # This is the typical price array
        self._typical_price_array = []
        # This is the pattern array which holds all the patterns
        self._pattern_array = array_data_tuple[0]
        # This is the buy performance array which is the pattern's outcome (same index as pattern)
        self._performance_array = array_data_tuple[1]
        # This is the array that has the historic data patterns that end up selling
        self._time = array_data_tuple[2]
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._high = array_data_tuple[4]
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._low = array_data_tuple[5]
        # This is the sell performance array which is the pattern's outcome (same index as pattern)
        self._close = array_data_tuple[6]