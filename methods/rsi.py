from enums import enums

class RSI:
    def __init__(self, close_prices, constant_class):
        self._close_prices = close_prices
        self._constants = constant_class
        self._period = self._constants.get_rsi_period()
        self._loss = []
        self._gain = []
        self._avg_gain = []
        self._avg_loss = []
        self._rs = []
        self._rsi = []

    def calculate_initial_arrays(self):
        # Calculate loss and gain arrays
        for i in range(len(self._close_prices)):
            try:
                diff = float(self._close_prices[i] - self._close_prices[i-1])
                if diff > 0:
                    self._gain.append(diff)
                elif diff < 0:
                    self._loss.append(abs(diff))
            except IndexError:
                pass

        # Calculate avg loss and gain first index
        self._avg_loss.append(float(sum(self._loss[0:self._period]) / self._period))
        self._avg_gain.append(float(sum(self._gain[0:self._period]) / self._period))

        # Calculate rest of avg loss and gain arrays
        for num in range(self._period+1, len(self._loss), 1):
            self._avg_loss.append(self.calculate_avg_difference(self._avg_loss[-1], self._loss[num]))
            self._avg_gain.append(self.calculate_avg_difference(self._avg_gain[-1], self._gain[num]))

        # Calculate rs array
        for n in range(len(self._avg_gain)):
            if self._avg_loss[n] == 0:
                self._rs.append(100)
            elif self._avg_gain[n] == 0:
                self._rs.append(0)
            else:
                self._rs.append(self._avg_gain[n] / self._avg_loss[n])

        # Calculate RSI array
        for ind in range(len(self._rs)):
            if self._avg_loss[ind] == 0:
                self._rsi.append(100)
            else:
                self._rsi.append(100-(100/(1+self._rs[ind])))

    def calculate_avg_difference(self, prev_avg, avg):
        return (prev_avg*(self._period-1)+avg)/self._period

    def add_point(self, close_point):
        # Add to close prices array
        self._close_prices.append(close_point)

        diff = float(self._close_prices[-1]) - float(self._close_prices[-2])
        if diff > 0:
            self._gain.append(diff)
        elif diff < 0:
            self._loss.append(abs(diff))

        self._avg_loss.append(self.calculate_avg_difference(self._avg_loss[-1], self._loss[-1]))
        self._avg_gain.append(self.calculate_avg_difference(self._avg_gain[-1], self._gain[-1]))

        if self._avg_loss[-1] == 0:
            self._rs.append(100)
        elif self._avg_gain[-1] == 0:
            self._rs.append(0)
        else:
            self._rs.append(self._avg_gain[-1] / self._avg_loss[-1])

        if self._avg_loss[-1] == 0:
            self._rsi.append(100)
        else:
            self._rsi.append(100 - (100 / (1 + self._rs[-1])))

    def get_result(self):
        """
        Returns the last value in the RSI array
        :return:
        """
        return self._rsi[-1]
