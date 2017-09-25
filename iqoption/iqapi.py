from iqoptionapi.api import IQOptionAPI
import time

class IQOptionApi:

    def __init__(self):
        self.api = IQOptionAPI("iqoption.com", "andrewskea.as@gmail.com", "PasswordTest98")
        self.api.connect()
        time.sleep(1)
        self.api.setactives([1])
        self.timesync = self.api.timesync

    def get_next_data_point(self):
        self.api.getcandles(1, 60)
        time.sleep(0.1)
        data = self.api.candles.candles_data
        return data[-2][2]

    def get_seconds_left(self):
        return self.timesync.server_datetime.second

    def sell(self, amount=1):
        self.api.buy(amount, 1, "turbo", "put")

    def buy(self, amount=1):
        self.api.buy(amount, 1, "turbo", "call")
