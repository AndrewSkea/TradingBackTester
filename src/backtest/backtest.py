import time

from terminaltables import AsciiTable

from . import method
from ..enums.enums import Option


class PatternRecognition:
    def __init__(self, data_array_class, time_ar, open_price, high_price, low_price, close_price, method_conf_json):
        self.data = data_array_class
        self._time = time_ar
        self._high = high_price
        self._low = low_price
        self._close = close_price
        self._open = open_price
        self.methods = [method.CustomMethod(data_array_class, method_conf_json)]
        self._bought_failed = 0
        self._bought_won = 0
        self._sold_failed = 0
        self._sold_won = 0
        self._starting_money = 100
        self._money = self._starting_money
        self._linear__money = self._starting_money
        self._linear_bet = 10
        self._lowest_money = self._starting_money
        self._return_rate = 0.78
        self._max_bet = 3000
        self._bet_percentage = 0.05

    def recognition(self, time_value, close_value, open_value, low_value, high_value, future_close_value):
        self.data.add_data(time_value=time_value, open_value=open_value,
                           close_value=close_value, low_value=low_value, high_value=high_value)
        [method.update_data_arrays() for method in self.methods]
        result = [method.get_result() for method in self.methods]
        if result.count(Option.BUY) > 0 and result.count(Option.SELL) == 0:
            result = Option.BUY
        elif result.count(Option.SELL) > 0 and result.count(Option.BUY) == 0:
            result = Option.SELL
        else:
            result = Option.NO_TRADE
        bet = min(self._bet_percentage * self._money, self._max_bet)
        if result == Option.BUY:
            if close_value < future_close_value:
                self._bought_won += 1
                self._money += bet * self._return_rate
                self._linear__money += self._linear_bet * self._return_rate
            elif close_value > future_close_value:
                self._bought_failed += 1
                self._money -= bet
                self._linear__money -= self._linear_bet
        elif result == Option.SELL:
            if close_value > future_close_value:
                self._sold_won += 1
                self._money += bet * self._return_rate
                self._linear__money += self._linear_bet * self._return_rate
            elif close_value < future_close_value:
                self._sold_failed += 1
                self._money -= bet
                self._linear__money -= self._linear_bet
        if self._money < self._lowest_money:
            self._lowest_money = self._money

    def start(self, num_trades):
        start_time = time.time()
        period = 1
        for index in range(len(self._close) - period):
            self.recognition(time_value=self._time[index],
                             close_value=self._close[index],
                             open_value=self._open[index],
                             low_value=self._low[index],
                             high_value=self._high[index],
                             future_close_value=self._close[index + period])
            if self._money < 1:
                print("Broke loop at the {}th minute because you are broke".format(index))
                break
        return self.log(start_time, num_trades)

    def log(self, start_time, num_trades):
        try:
            total = self._bought_won + self._sold_won + self._bought_failed + self._sold_failed
            num_won = self._bought_won + self._sold_won
            num_lost = self._bought_failed + self._sold_failed
            per_win = int((100 * num_won / total) if total != 0 else 0)
            bought_per_win = int(100 * self._bought_won / (self._bought_won + self._bought_failed))
            sold_per_win = int(100 * self._sold_won / (self._sold_failed + self._sold_won))
            final__money_string = "£{:,}".format(int(self._money - self._starting_money)) \
                .replace(',', "'")

            with open('src/logs/log.txt', 'a') as log_file:
                log_str = "\nTime\t\t{}s\nTrades\t\t{}\nIdeal Trades\t{}\nProfit\t\t{}" \
                          "\nLinear Profit\t£{}\nLowest\t\t£{}\n{}".format(int(time.time() - start_time),
                                                                           total,
                                                                           num_trades,
                                                                           final__money_string,
                                                                           int(self._linear__money),
                                                                           int(self._lowest_money), AsciiTable([
                        ["Result", "Bought", "Sold", "Total"],
                        ["Won", self._bought_won, self._sold_won, num_won],
                        ["Failed", self._bought_failed, self._sold_failed, num_lost],
                        ["Totals", str(bought_per_win) + "%", str(sold_per_win) + "%",
                         str(per_win) + "%"]]).table)
                log_file.write(log_str)
                print(log_str)
            return {
                "time": int(time.time() - start_time),
                "total": total,
                "num_bought_win": self._bought_won,
                "num_bought_lost": self._bought_failed,
                "num_sold_win": self._sold_won,
                "num_sold_lost": self._sold_failed,
                "profit": int(self._money - self._starting_money),
                "linear_profit": int(self._linear__money),
                "lowest_money": int(self._lowest_money)
            }
        except ZeroDivisionError:
            print("Divided by zero")
            return None
