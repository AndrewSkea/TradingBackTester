from datetime import datetime


class Dataset(object):
    """
    Contains data about a consecutive series of data points.
    """

    def __init__(self, data):
        """
        Sets the data in this dataset.
        :param data: A list of elements, where each element is in the format [date, open, high, low, close] and each
        piece of data is a string.
        """
        self._size = len(data)
        self._dates = [datetime.strptime(x[0], "%Y%m%d %H%M%S") for x in data]
        self._opens = [float(x[1]) for x in data]
        self._highs = [float(x[2]) for x in data]
        self._lows = [float(x[3]) for x in data]
        self._closes = [float(x[4]) for x in data]

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
