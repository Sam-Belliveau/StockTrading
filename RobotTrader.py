###
### This file contains robots that talk to brokers
### and buy and sell stock
###
### Sam Belliveau
###

import BrokerSim
import StockSim
import SmoothAlgo

# Robot that smooths out the stock 
# price and looks at trends
class TrendRobot:
    
    ####################
    ### INITIALIZING ###
    ####################

    def __init__(self, broker, smoother, buy_rate=1, sell_rate=1, buy_margin=1, sell_margin=1):
        self._broker = broker
        self._smoother = smoother

        self._price = None
        self._smoothed_price = None

        self._buy_rate = buy_rate
        self._sell_rate = sell_rate
        self._buy_margin = buy_margin
        self._sell_margin = sell_margin

    
    ##################
    ### SIMULATING ###
    ##################

    # Check if there is more trading to do
    def done(self):
        return not self._broker.has_next_price()

    # Buy and trade stock for that day
    def simulate_day(self):
        # Go to the next price value
        self._broker.update_stock_price()

        # Update price and smoothed price
        self._price = self._broker.get_stock_price()
        self._smoothed_price = self._smoother.smooth(self._price)

        # If stock is doing worse than trend, sell
        if self._price < self._smoothed_price * self._sell_margin:
            self._broker.sell_stock(self._sell_rate)

        # If stock is doing better than trend, buy
        if self._price > self._smoothed_price * self._buy_margin:
            self._broker.buy_stock(self._buy_rate)


    ###########################
    ### GETTING INFORMATION ###
    ###########################

    # Get amount of money in wallet, without stocks
    def get_raw_wallet(self):
        return self._broker.get_raw_wallet()

    # Get number of stocks held
    def get_stocks_held(self):
        return self._broker.get_stocks_held()

    # Get total amount of money in wallet, stocks included
    def get_total_wallet(self):
        return self._broker.get_total_wallet()

    # Get the current price of the stock
    def get_stock_price(self):
        return self._price

    # Get the smoothed version of price
    def get_smooth_stock_price(self):
        return self._smoothed_price

    # Return broker variable
    def get_broker(self):
        return self._broker


# Robot that looks at two trends and 
# buys and sells based on thant
class DualTrendRobot(TrendRobot):
    
    ####################
    ### INITIALIZING ###
    ####################

    def __init__(self, broker, buy_smoother, sell_smoother, buy_rate=1, sell_rate=1, buy_margin=1, sell_margin=1):
        self._broker = broker
        self._buy_smoother = buy_smoother
        self._sell_smoother = sell_smoother

        self._price = None
        self._buy_smoothed_price = None
        self._sell_smoothed_price = None

        self._buy_rate = buy_rate
        self._sell_rate = sell_rate
        self._buy_margin = buy_margin
        self._sell_margin = sell_margin

    
    ##################
    ### SIMULATING ###
    ##################

    # Buy and trade stock for that day
    def simulate_day(self):
        # Go to the next price value
        self._broker.update_stock_price()

        # Update price and smoothed price
        self._price = self._broker.get_stock_price()
        self._buy_smoothed_price = self._buy_smoother.smooth(self._price)
        self._sell_smoothed_price = self._sell_smoother.smooth(self._price)

        # If stock is doing better than trend, buy
        if self._price > self._buy_smoothed_price * self._buy_margin:
            self._broker.buy_stock(self._buy_rate)

        # If stock is doing worse than trend, sell
        if self._price < self._sell_smoothed_price * self._sell_margin:
            self._broker.sell_stock(self._sell_rate)


    ###########################
    ### GETTING INFORMATION ###
    ###########################

    # Get the smoothed version of price
    def get_smooth_stock_price(self):
        return self._buy_smoothed_price

    # Get the smoothed version of price for buying
    def get_buy_smooth_stock_price(self):
        return self._buy_smoothed_price

    # Get the smoothed version of price for selling
    def get_sell_smooth_stock_price(self):
        return self._sell_smoothed_price