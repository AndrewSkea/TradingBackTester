import importlib
from ..enums.enums import Option
from .. import indicators

class CustomMethod:
    def __init__(self, data_array_class, json_config):
        """
        Parsing the json string to instantiate what indicators and signals are required
        Gets the signal list
        Updates all the data and return a result
        :param data_array_class: Data array class
        :param json_config: Json config detailing indicators and signals used
        """
        self.indicator_list = {}
        self.signals_list = {}
        for key in json_config['indicators']:
            self.signals_list[key] = json_config['indicators'][key]['signals']
            self.indicator_list[key] = importlib.import_module('indicators.' + str(key)).get_class_instance(
                data_array_class, **json_config['indicators'][key])

    def update_data_arrays(self):
        [indicator.update_data_arrays() for indicator in self.indicator_list.values()]

    def get_result(self):
        for key, value in self.indicator_list.items():
            if value.is_valid_trading_time:
                if all([getattr(value, signal)(**params) for signal, params in self.signals_list[key]['BUY'].items()]):
                    return Option.BUY
                elif all([getattr(value, signal)(**params) for signal, params in self.signals_list[key]['SELL'].items()]):
                    return Option.SELL
        return Option.NO_TRADE
