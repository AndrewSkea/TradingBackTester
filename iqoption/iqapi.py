# from iqoptionapi.api import IQOptionAPI
import time


class IQOptionApi:
    def __init__(self):
        self.api = IQOptionAPI("iqoption.com", "andrewskea.as@gmail.com", "PasswordTest98")
        self.api.connect()
        time.sleep(1)
        self.api.setactives([1])  # This means it using EURUSD
        self.timesync = self.api.timesync
        print('This is connected')

    def get_next_data_point(self):
        self.api.getcandles(1, 60)
        curr_time = time.time()
        while abs(curr_time - time.time()) < 1.25:
            if self.api.candles.candles_data is not None:
                break
        data = self.api.candles.candles_data
        if data is not None:
            data = self.api.candles.candles_data
            data_array = [item for item in data if item[2] != 0][-1]
            datetime = data_array
            open_price = float(data_array[1]/1000000.0)
            high = float(data_array[2]/1000000.0)
            low = float(data_array[3]/1000000.0)
            close = float(data_array[4]/1000000.0)
            return [datetime, open_price, high, low, close]
        else:
            return None

    def get_seconds_left(self):
        return self.timesync.server_datetime.second

    def sell(self, amount=1):
        self.api.buy(amount, 1, "turbo", "put")

    def buy(self, amount=1):
        self.api.buy(amount, 1, "turbo", "call")
