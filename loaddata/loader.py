from datetime import time, datetime, timedelta, MINYEAR
import numpy as np
from loaddata.dataset import Dataset


class Loader(object):
    """
    Utility designed to load in the backtest data from a csv file into a set of lists.
    """

    def __init__(self):
        """
        Loads the data into memory.
        """
        self._data = []
        self._size = []
        self._dates = []
        self._opens = []
        self._highs = []
        self._lows = []
        self._closes = []
        self._datasets = []

    def load_data(self, max_candles_needed_for_first_point, mon=True, tue=True, wed=True, thu=True, fri=True, sat=False,
                  sun=False, start_hour=0, start_min=0, end_hour=23, end_min=59):
        """
        Loads in the raw data from the csv file and converts that into a single list of tuples, where each tuple is an
        entry in the csv file.
        The list is ordered chronologically.
        """
        raw_data = np.loadtxt('eurusd.csv',
                              delimiter=',',
                              comments='#',
                              usecols=(0, 1, 2, 3, 4),
                              dtype=str)
        # Loads the file into a list of tuples, each tuple in the following format
        # (date, open, high, low, close)
        # Each element in each tuple is a string at this stage.
        for i in range(raw_data.shape[0]):
            self._data.append(tuple(np.ndarray.tolist(raw_data[i, :])))
        dates = [datetime.strptime(x[0], "%Y%m%d %H%M%S") for x in self._data]
        print(dates[0])

        # Removes any elements from data where the date is not in the required range.
        start_time = (datetime(1, 1, MINYEAR, hour=start_hour, minute=start_min) - timedelta(
            minutes=max_candles_needed_for_first_point)).time()
        i = 0
        for date in dates:
            if (not (start_time <= date.time() < time(end_hour, end_min, 0))) or \
                    (not mon and date.weekday() == 0) or \
                    (not tue and date.weekday() == 1) or (not wed and date.weekday() == 2) or \
                    (not thu and date.weekday() == 3) or (not fri and date.weekday() == 4) or \
                    (not sat and date.weekday() == 5) or (not sun and date.weekday() == 6):
                self._data.pop(i)
            else:
                i += 1

        # Populates the lists of all the data that we are interested in.
        self._size = len(self._data)
        self._dates = [datetime.strptime(x[0], "%Y%m%d %H%M%S") for x in self._data]
        self._opens = [float(x[1]) for x in self._data]
        self._highs = [float(x[2]) for x in self._data]
        self._lows = [float(x[3]) for x in self._data]
        self._closes = [float(x[4]) for x in self._data]

        # Splits the data up into datasets, one for each individual day.
        start_of_current_day = 0
        current_day = self._dates[0].day
        for i in range(len(self._data)):
            if self._dates[i].day != current_day:
                self._datasets.append(Dataset(self._data[start_of_current_day:i]))
                current_day = self._dates[i].day
                start_of_current_day = i
        self._datasets.append(Dataset(self._data[start_of_current_day:]))

    def get_number_of_data_points(self):
        return self._size

    def get_dates(self):
        return self._dates

    def get_opens(self):
        return self._opens

    def get_highs(self):
        return self._highs

    def get_lows(self):
        return self._lows

    def get_closes(self):
        return self._closes

    def get_datasets(self):
        return self._datasets
