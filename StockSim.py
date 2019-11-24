###
### This file creates a stock class that the brokers
### will use to deliver their data to their interface
###
### Sam Belliveau
###

from datetime import datetime
import pandas
import pandas_datareader.data as web

# This class holds the basic outline of
# how the stock should be interacted with
class Stock:
    def update_price(self):
        pass

    def get_price(self):
        pass

    def has_next_price(self):
        return True

# This class extends the stock class and
# feeds it historical data based on ticker
class HistoricalStock(Stock):
    def _get_share_data(self, ticker, start=datetime(2010,1,1), end=datetime.now()):
        data = web.DataReader(ticker, 'yahoo', start, end)
        return data['Adj Close']

    # Get stock data from yahoo, store all of it
    def __init__(self, ticker, start=datetime(2010,1,1)):
        self._ticker = ticker.upper().strip()
        self._share_data = self._get_share_data(ticker, start=start)
        self._max_day = len(self._share_data.values)
        self._day = 0

    # Go to next day
    def update_price(self):
        self._day = min(self._day + 1, self._max_day - 1)

    # If we are done with data
    def has_next_price(self):
        return (self._day + 1) < self._max_day

    # Get the price of the stock based on day
    def get_price(self):
        return self._share_data.values[self._day]
    
    # Get the date of the price
    def get_date(self):
        return self._share_data.index[self._day]

    # Raw share data just in case its needed
    def get_raw_share_data(self):
        return self._share_data
