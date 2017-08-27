import datetime
import time

from databases import DBHandler
import enums


class LogHandler(DBHandler):
    """
    This creates and interacts with the logs database to store and retrieve data
    It stores all logs from buys or sells and the attached information

    Table columns: current_time, option, number_of_patterns
                average_predicted_outcome, time_for_recognition,
                number_of_bets, number_down_arrays, number_up_arrays,
    """

    def __init__(self):
        """
        Sets up the variable for the class
        """
        super(self.__class__, self).__init__()
        self.connect()

    def insert(self, num_patterns, avg_predicted_outcome, time_for_recog, num_bets, num_down_arrays,
               num_up_arrays):
        """
        this sets up the insert string that will be executed
        :return: null
        """
        print 'Inserting into log started'
        _date_time = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        _insert_string = 'INSERT INTO log VALUES ((SELECT MAX(id)+1 FROM log),{},{},{},{},{},{},{});' \
            .format("'" + _date_time + "'", num_patterns, avg_predicted_outcome, time_for_recog, num_bets,
                    num_down_arrays,
                    num_up_arrays)
        self.execute(_insert_string, statement_type=enums.StatementType.INSERT)

    def select(self, select_type=enums.StatementType.SELECT, amount=300):
        """
        This sets up the select string that will be executed
        :return: null
        """
        _date_time = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        _date_time = _date_time[0:10]
        if select_type == 0:
            _select_string = 'SELECT cur_time,' \
                             'num_patterns, ' \
                             'avg_predicted_outcome, ' \
                             'time_for_recog, ' \
                             'num_bets, ' \
                             'num_down_arrays, ' \
                             'num_up_arrays, ' \
                             'FROM logs' \
                             'WHERE curr_time like {}'.format("'%" + _date_time + "%'")

        return self.execute(_select_string, statement_type=enums.StatementType.SELECT)
