from databases.db_handler import DBHandler
import os
import numpy as np
import time
import datetime

import enums
from databases import DBHandler


class HistDBHandler(DBHandler):
    """
    This creates and interacts with the historic data table to store and retrieve data
    It stores all the data for the pst x months

    Table columns: id, current_time, close_price
    """

    def __init__(self):
        """
        Sets up the variable for the class
        """
        super(self.__class__, self).__init__()
        self.connect()

    def insert(self, close_price):
        """
        this sets up the insert string that will be executed
        :return: null
        """
        _date_time = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        _insert_string = 'INSERT INTO histdata VALUES ((SELECT MAX(id)+1 FROM log),{},{})'\
            .format(_date_time, close_price)
        self.execute(_insert_string, enums.StatementType.INSERT)

    def select(self):
        """
        This sets up the select string that will be executed
        :return: null
        """
        # Sets the select string statement so that it gets the current time and the prices from histdata table
        _select_string = 'SELECT close_prices FROM histdata'
        return self.execute(_select_string, enums.StatementType.SELECT)


    def get_all_data(self, amount=250000):
        # Set select string for getting all data from the database
        _select_string = 'SELECT close_prices FROM histdata LIMIT {}'.format(amount)
        # Get data from execute function
        _query_result = self.execute(string=_select_string, statement_type=enums.StatementType.SELECT)
        # Initialise aan empty array to hold the final array of data
        _prices_array = []
        # This is the final array that contains only the values
        [_prices_array.append(float(_query_result[i][0])) for i in range(len(_query_result))]
        # return the array with just numbers (This is done because it is formatted as [(1.8328239,),(1.8328239,),...]
        return _prices_array
