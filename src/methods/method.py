import json
import importlib

from enums.enums import Option
from indicators.cci import CCI
from indicators.adx import ADX
from indicators.bollingerbands import BollingerBands
from indicators.awesome_oscillator import AwesomeOscillator
from indicators.ema import EMA
from indicators.macd import MACD
from indicators.rsi import RSI
from indicators.sma import SMA
from indicators.stochastic_oscillator import StochasticOscillator
from indicators.typical_price import TypicalPrice
from indicators.wma import WMA


class CustomMethod:
    def __init__(self, data_array_class, json_config):
        """
        Parsing the json string to instantiate what indicators and signals are required
        Gets the signal list
        Updates all the data and return a result
        :param data_array_class: Data array class
        :param json_config: Json config detailing indicators and signals used
        """
        json_dict = json.loads(json_config)
        self.indicator_list = []
        self.signals_list = []
        for key in json_dict:
            self.signals_list.append(json_dict[key]['signals'])
            self.indicator_list.append(importlib.import_module('indicators.' + key).
                                       get_class_instance(data_array_class, **json_dict[key]))

    def update_data_arrays(self):
        [indicator.update_data_arrays() for indicator in self.indicator_list]

    def get_result(self):
        if any([ind.is_trading_time() for ind in self.indicator_list]):
            for i in range(len(self.indicator_list)):
                if all([getattr(self.indicator_list[i], signal)() for signal in self.signals_list[i]['BUY']]):
                    return Option.BUY
                elif all([getattr(self.indicator_list[i], signal)() for signal in self.signals_list[i]['SELL']]):
                    return Option.SELL
        return Option.NO_TRADE
