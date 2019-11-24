from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import pandas

# My classes for simulating trading
import SmoothAlgo as SAlgo
from StockSim import HistoricalStock
from BrokerSim import Broker
from RobotTrader import TrendRobot

############################
###### BEGIN : CONFIG ######
############################

TICKER = 'amd'
START = datetime(2015,1,1)

START_WALLET = 50000

BUY_RATE = 10
BUY_MARGIN = 1.05

SELL_RATE = 16
SELL_MARGIN = 1.01

# SMOOTH_ALGO = SAlgo.MovingAverage(32)
# SMOOTH_ALGO = SAlgo.WeightedMovingAverage(32)
SMOOTH_ALGO = SAlgo.ExponentialMovingAverage(12)

############################
####### END : CONFIG #######
############################

### The amount that the data will be scaled on the graph
STOCKS_HELD_SCALE = 10
WALLET_SCALE = 1000

### Get the stock data into a class called my_stock ###
my_stock = HistoricalStock(ticker=TICKER, start=START)

### Simulate broker that holds all the money and my stocks ###
my_broker = Broker(stock=my_stock, wallet=START_WALLET)

### Create robot class and give it all the parameters ###
my_robot = TrendRobot(
    broker=my_broker, smoother=SMOOTH_ALGO, 
    buy_rate=BUY_RATE, sell_rate=SELL_RATE,
    buy_margin=BUY_MARGIN, sell_margin=SELL_MARGIN
)

### Keep track of data in these classes ###
stocks_held = {}
total_wallet = {}
raw_wallet = {}
raw_stock_price = {}
smooth_stock_price = {}

### While there is still stock data,   ###
### Get the robot to go through it and ###
### record the data                    ###
while not my_robot.done():
    # Get robot to buy and sell for the day
    my_robot.simulate_day()

    # Get the current date from the stock class
    date = my_stock.get_date()

    # Get the amount of stocks held
    stocks_held[date] = my_robot.get_stocks_held() / STOCKS_HELD_SCALE

    # Get the wallet amount with and without stocks in them
    total_wallet[date] = my_robot.get_total_wallet() / WALLET_SCALE
    raw_wallet[date] = my_robot.get_raw_wallet() / WALLET_SCALE

    # get the raw and the stock prices
    raw_stock_price[date] = my_robot.get_stock_price()
    smooth_stock_price[date] = my_robot.get_smooth_stock_price()

# Plot all of the data
pandas.Series(raw_stock_price).plot(label='Stock Price')
pandas.Series(smooth_stock_price).plot(label='Smooth Stock Price')
pandas.Series(total_wallet).plot(label='Total Wallet / ' + str(WALLET_SCALE))
pandas.Series(raw_wallet).plot(label='Wallet / ' + str(WALLET_SCALE))
#pandas.Series(stocks_held).plot(label='Stocks Held / ' + str(STOCKS_HELD_SCALE))

# Show trading information
plt.legend()
plt.show()