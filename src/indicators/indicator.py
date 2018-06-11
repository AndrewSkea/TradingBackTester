from abc import abstractmethod
from ..logs.print import _print


class Indicator:
    def __init__(self, data_array_class, time_limits):
        self._data = data_array_class
        self._time_limits = time_limits
        self.is_valid_trading_time = False
        _print(self.__str__())

    @abstractmethod
    def __str__(self):
        pass

    def is_trading_time(self):
        return self.is_valid_trading_time

    def update_data_arrays(self):
        self.is_valid_trading_time = self._data.time[-1].tm_wday <= 4 \
                                     and any(tup[0] <= self._data.time[-1].tm_hour < tup[1] for tup in self._time_limits)

    @abstractmethod
    def has_broken_above(self, *args, **kwargs):
        pass

    @abstractmethod
    def has_broken_below(self, *args, **kwargs):
        pass

    @abstractmethod
    def has_come_back_in_from_above(self, *args, **kwargs):
        pass

    @abstractmethod
    def has_come_back_in_from_below(self, *args, **kwargs):
        pass

    @abstractmethod
    def has_moved_up_for(self, *args, **kwargs):
        pass

    @abstractmethod
    def has_moved_down_for(self, *args, **kwargs):
        pass

    @abstractmethod
    def is_above(self, *args, **kwargs):
        pass

    @abstractmethod
    def is_below(self, *args, **kwargs):
        pass

    @abstractmethod
    def is_between(self, *args, **kwargs):
        pass


@abstractmethod
def get_class_instance(data_class, **kwargs):
    pass
