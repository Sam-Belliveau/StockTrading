###
### This file is where the broker is defined, the broker
### is what the robots will trade with and it keeps track 
### of things
###
### Sam Belliveau
###

import StockSim

# This class simulates a stock broker and your wallet
class Broker:
    
    ####################
    ### INITIALIZING ###
    ####################

    def __init__(self, stock, wallet=50000, fee=0):
        self._stock = stock
        self._stocks_held = 0
        self._wallet = wallet
        self._fee = fee
    

    ############################
    ### GETTING STOCK PRICES ###
    ############################

    def update_stock_price(self):
        self._stock.update_price()

    def get_stock_price(self):
        return self._stock.get_price()

    def has_next_price(self):
        return self._stock.has_next_price()
    

    ################################
    ### BUYING AND SELLING STOCK ###
    ################################

    def buy_stock(self, amount=1):
        # Get stock price and cap the requested amount
        stock_price = self.get_stock_price()
        capped_amount = round(min(self._wallet // stock_price, amount))

        # Add stocks to stocks held and remove from wallet
        self._stocks_held += capped_amount
        self._wallet -= stock_price * capped_amount / (1 - self._fee)

    def sell_stock(self, amount=1):
        # Get stock price and cap the requested amount
        stock_price = self.get_stock_price()
        capped_amount = round(min(self._stocks_held, amount))

        # Remove stocks to stocks held and add to wallet
        self._stocks_held -= capped_amount
        self._wallet += stock_price * capped_amount * (1 - self._fee)

    ###########################
    ### GETTING INFORMATION ###
    ###########################

    # Get amount of money in wallet, without stock
    def get_raw_wallet(self):
        return self._wallet

    # Get total number of stocks held
    def get_stocks_held(self):
        return self._stocks_held

    # Get the amount of money held in stocks only
    def get_held_stocks_prices(self):
        return self.get_stocks_held() * self.get_stock_price()

    # Get total amount of money in wallet, with stock
    def get_total_wallet(self):
        return self.get_raw_wallet() + self.get_held_stocks_prices()