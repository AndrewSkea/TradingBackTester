import terminaltables
from enums.enums import Option, Position, Trend
from indicators import cci, bollingerbands, rsi
from constants import finalconstants as const


class CustomFour:
    def __init__(self, data_array_class):
        """
        Combination of BBAND, CCI and RSI
        """
        self._data = data_array_class
        self.constants = const
        self._rsi_class = rsi.RSI(self._data)
        self._cci_class = cci.CCI(self._data)
        # self._bband_class = bollingerbands.BollingerBands(self._data)
        self._num = 0
        self._result_table = [
            ['High', 'Low', 'Close', 'CCI', 'TP', 'TP_SMA', 'MeanDev', 'BBAND_L', 'BBAND_M', 'BBAND_U', 'RSI']]

        # self._file = open('/testing/eurusd_final_results_output.csv', 'a')

    def update_data_arrays(self):
        self._rsi_class.update_data_arrays()
        self._cci_class.update_data_arrays()
        # self._bband_class.update_data_arrays()

    def add_to_table_print(self):
        self._result_table.append([
            self._data.high[-1],
            self._data.low[-1],
            self._data.close[-1],
            self._cci_class.cci[-1],
            self._data.typical_price[-1],
            self._cci_class.typical_price_sma.get_sma_array()[-1],
            self._cci_class.mean_deviation_typical_price[-1],
            self._bband_class.lower_band[-1],
            self._bband_class.middle_band.get_sma_array()[-1],
            self._bband_class.upper_band[-1],
            self._rsi_class.rsi[-1]
        ])

    def get_result(self):
        if self._cci_class.has_broken_out() == Position.JUST_GONE_ABOVE or self._rsi_class.has_broken_out() == Position.JUST_GONE_ABOVE:
            return Option.SELL
        elif self._cci_class.has_broken_out() == Position.JUST_GONE_BELOW or self._rsi_class.has_broken_out() == Position.JUST_GONE_BELOW:
            return Option.BUY
        else:
            return Option.NO_TRADE

        # if self._rsi_class.has_broken_out() == Position.JUST_GONE_ABOVE:
        #     return Option.SELL
        # elif self._rsi_class.has_broken_out() == Position.JUST_GONE_BELOW:
        #     return Option.BUY
        # else:
        #     return Option.NO_TRADE