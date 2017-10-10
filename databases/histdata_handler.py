import enums
from databases import DBHandler


class HistDBHandler(DBHandler):
    """
    This creates and interacts with the historic data table to store and retrieve data
    It stores all the data for the pst x months

    Table columns: id, current_time, close_price
    """

    def __init__(self, constants_class):
        """
        Sets up the variable for the class
        """
        super(self.__class__, self).__init__()
        self.connect()
        self.constants_class = constants_class

    def get_all_data(self):
        # Set select string for getting all data from the database
        _select_string = 'SELECT * FROM all_past_data WHERE id < (SELECT MAX(id)-{} FROM all_past_data) LIMIT {}'\
            .format(self.constants_class.get_num_live_patterns(), self.constants_class.get_num_data_points())
        # Get data from execute function
        return self.execute(string=_select_string, statement_type=enums.StatementType.SELECT)

    def get_all_pattern_data(self):
        # Set select string for getting all data from the database - ID is opposite way to time
        _select_string = 'SELECT * FROM all_past_data where id > (SELECT MAX(id)-{} FROM all_past_data)'\
            .format(self.constants_class.get_num_live_patterns())
        # Get data from execute function
        return self.execute(string=_select_string, statement_type=enums.StatementType.SELECT)

    def get_all_data_for_indicators(self):
        # Set select string for getting all data from the database - ID is opposite way to time
        _select_string = 'SELECT * FROM all_past_data where id > (SELECT MAX(id)-{} FROM all_past_data) LIMIT {}'\
            .format(self.constants_class.get_num_data_points_for_indicators(),
                    self.constants_class.get_num_data_points_for_indicators())
        # Get data from execute function
        return self.execute(string=_select_string, statement_type=enums.StatementType.SELECT)

