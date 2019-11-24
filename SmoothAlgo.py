###
### This file contains algortihms that robots 
### will use to smooth out stock prices
###
### Sam Belliveau
###

# Base smoothing class that every other algorithm will fit into
class Smoother:
    def smooth(self, next_price):
        pass

# Moving Average Smoother Class
class MovingAverage(Smoother):
    def __init__(self, size):
        self._values = []
        self._max_size = size

    def smooth(self, next_price):
        self._values += [float(next_price)]
        if len(self._values) > self._max_size:
            self._values.pop(0)
        
        return sum(self._values) / len(self._values)

# Weighted Moving Average Smoother Class
class WeightedMovingAverage(Smoother):
    def __init__(self, size):
        self._values = [0]
        self._max_size = size

    def smooth(self, next_price):
        self._values += [float(next_price)]
        if len(self._values) > self._max_size:
            self._values.pop(0)
        
        divisor = 0; total = 0
        for i in range(0, len(self._values)):
            divisor += i
            total += i * self._values[i]
        return total / divisor

# Exponential Moving Average Smoother Class
class ExponentialMovingAverage(Smoother):
    def __init__(self, exp):
        self._exp = exp
        self._last_value = None

    def smooth(self, next_price):
        if self._last_value == None:
            self._last_value = next_price
        
        self._last_value += (next_price - self._last_value) / self._exp
        return self._last_value