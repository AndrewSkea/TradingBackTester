import sqlite3
import os

from abc import abstractmethod
from enums import enums


class DBHandler(object):
    """
    This is the base class for all databases to inherit from
    All methods are overridable if required
    """

    def __init__(self):
        """
        Constructor for setting up the base variables.
        """
        # The database name
        self._database = str(os.getcwd() + '\databases\iqoption.sql')
        # Is it connected to the database
        self._connected = False
        # The connection to the database
        self._connection = None
        # The cursor to interact with the database
        self._cursor = None
        # Connect to the database
        self.connect()

    def connect(self):
        """
        This initialises the connection to the database and sets var for cursor
        :return: null
        """
        self._connection = sqlite3.connect(self._database)
        self._cursor = self._connection.cursor()
        self._connected = True

    @abstractmethod
    def insert(self, *args, **kwrds):
        """
        this sets up the insert string that will be executed
        :return: null
        """
        pass

    @abstractmethod
    def select(self):
        """
        This sets up the select string that will be executed
        :return: null
        """
        pass

    def execute(self, string, statement_type=enums.StatementType.SELECT):
        """
        This executes the paramater string on the database
        :param statement_type: type of statement that will be executed on the database
        :param string: the string that will be executed
        :return: the list of selected data if a select statement was executed, else nothing
        """
        self._cursor.execute(string)
        self._connection.commit()
        if statement_type == enums.StatementType.SELECT:
            return self._cursor.fetchall()
