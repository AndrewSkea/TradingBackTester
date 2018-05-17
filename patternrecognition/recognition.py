import time
from methods import custom_four as C4
from terminaltables import AsciiTable
from enums.enums import Option, Indicators
from graph.graph import LiveGraph
from constants import finalconstants as const


class PatternRecognition:
    def __init__(self, data_array_class, time_ar, open_price, high_price, low_price, close_price):

        self.data = data_array_class
        self._time = time_ar
        self._high = high_price
        self._low = low_price
        self._close = close_price
        self._open = open_price

        self.method = C4.CustomFour(self.data)
        self._bought_failed = 0
        self._bought_won = 0
        self._sold_failed = 0
        self._sold_won = 0
        self._starting_money = 100
        self._money = self._starting_money
        self._lowest_money = self._starting_money
        self._return_rate = 0.78
        self._max_bet = 3000
        self._bet_percentage = 0.05

    def recognition(self, time_value, close_value, open_value, low_value, high_value, future_close_value):
        self.data.add_data(time_value=time_value, open_value=open_value,
                           close_value=close_value, low_value=low_value, high_value=high_value)
        self.method.update_data_arrays()
        result = self.method.get_result()
        bet = min(self._bet_percentage * self._money, self._max_bet)
        if result == Option.BUY:
            if close_value < future_close_value:
                self._bought_won += 1
                self._money += bet * self._return_rate
            elif close_value > future_close_value:
                self._bought_failed += 1
                self._money -= bet
        elif result == Option.SELL:
            if close_value > future_close_value:
                self._sold_won += 1
                self._money += bet * self._return_rate
            elif close_value < future_close_value:
                self._sold_failed += 1
                self._money -= bet
        if self._money < self._lowest_money:
            self._lowest_money = self._money

    def start(self):
        start_time = time.time()
        num_iterations = len(self._close)
        for index in range(num_iterations - 5):
            self.recognition(time_value=self._time[index],
                             close_value=self._close[index],
                             open_value=self._open[index],
                             low_value=self._low[index],
                             high_value=self._high[index],
                             future_close_value=self._close[index + 1])
            if self._money < 1:
                print("Broke loop at the {}th minute because you are broke".format(index))
                break
        self.log(start_time)

    def log(self, start_time):
        try:
            print("Logging Results")
            total = self._bought_won + self._sold_won + self._bought_failed + self._sold_failed
            num_won = self._bought_won + self._sold_won
            num_lost = self._bought_failed + self._sold_failed
            per_win = int((100 * num_won / total) if total != 0 else 0)
            bought_per_win = int(100 * self._bought_won / (self._bought_won + self._bought_failed))
            sold_per_win = int(100 * self._sold_won / (self._sold_failed + self._sold_won))
            final__money_string = "£{:,}".format(int(self._money-self._starting_money))\
                .replace(',', "'")

            with open('logdata/log.txt', 'a') as log_file:
                log_str = "\nAfter {}s, {} trades, net profit of {} and lowest money reached: £{}\n{}"\
                    .format(int(time.time() - start_time), total, final__money_string, self._lowest_money, AsciiTable([
                                ["Result", "Bought", "Sold", "Total"],
                                ["Won", self._bought_won, self._sold_won, num_won],
                                ["Failed", self._bought_failed, self._sold_failed, num_lost],
                                ["Totals", str(bought_per_win) + "%", str(sold_per_win) + "%",
                                 str(per_win) + "%"]]).table)
                log_file.write(log_str)
                print(log_str)
        except ZeroDivisionError:
            print("Divided by zero")


