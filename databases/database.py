import sqlite3
import os
import time
import random


class Database:
    """
    This is the base class for all databases to inherit from
    All methods are overridable if required
    """

    def __init__(self):
        """
        Constructor for setting up the base variables.
        """
        # The database name
        self._database = str(os.getcwd() + '/databases/iqoption.sql')
        # Is it connected to the database
        self._connected = False
        # The connection to the database
        self._connection = None
        # The cursor to interact with the database
        self._cursor = None
        # Run connect method
        self.connect()

    def connect(self):
        """
        This initialises the connection to the database and sets var for cursor
        :return: null
        """
        self._connection = sqlite3.connect(self._database)
        self._cursor = self._connection.cursor()
        self._connected = True

    def execute(self, string):
        """
        This executes the paramater string on the database
        :param string: the string that will be executed
        :return: null
        """
        self._cursor.execute(string)
        self._connection.commit()

    def create_database(self):
        """
        Creates a database to store the logs and data in
        :return: null
        """
        # This is the creation string for the database
        # creation_string = 'CREATE DATABASE IF NOT EXISTS iqoption'
        # Calls the execute function with this string
        # self.execute(_creation_string)
        # Calls create log table within db
        self.create_log_table()
        # Calls create histdata within db
        self.create_histdata_table()

    def create_log_table(self):
        """
        This creates the log table if it doesn't already exist in the database
        by creating a string and then executing it
        :return: null
        """
        _creation_string = 'CREATE TABLE IF NOT EXISTS `log` (' \
                           '`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                           '`cur_time`	TEXT NOT NULL,' \
                           '`num_patterns`	INT NOT NULL,' \
                           '`avg_predicted_outcome`	REAL NOT NULL,' \
                           '`time_for_recog`	REAL NOT NULL,' \
                           '`num_bets`	INT NOT NULL,' \
                           '`num_down_arrays`	INT NOT NULL,' \
                           '`num_up_arrays`	INT NOT NULL' \
                           ');'
        self.execute(_creation_string)

    def create_histdata_table(self):
        """
        This creates the histdata table if it doesn't already exist in the database
        by creating a string and then executing it
        :return: null
        """
        _creation_string = 'CREATE TABLE IF NOT EXISTS `histdata` (' \
                           '`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                           '`curr_time`	TEXT,' \
                           '`close_prices`	REAL' \
                           ');'
        self.execute(_creation_string)
