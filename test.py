from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import pandas

# My classes for simulating trading
import SmoothAlgo as SAlgo
from StockSim import HistoricalStock
from BrokerSim import Broker
from RobotTrader import DualTrendRobot
from RobotTrader import TrendRobot

############################
###### BEGIN : CONFIG ######
############################

TICKER = 'amd'
START = datetime(2010,1,1)

START_WALLET = 50000

BUY_RATE = 13
BUY_MARGIN = 1.05

SELL_RATE = 21
SELL_MARGIN = 0.975

DUAL_ALGORITHM = False

if DUAL_ALGORITHM:
    BUY_SMOOTH_ALGO = SAlgo.MovingAverage(50)
    SELL_SMOOTH_ALGO = SAlgo.ExponentialMovingAverage(8)
else:
    # SMOOTH_ALGO = SAlgo.MovingAverage(50)
    # SMOOTH_ALGO = SAlgo.WeightedMovingAverage(32)
    SMOOTH_ALGO = SAlgo.ExponentialMovingAverage(16)

############################
####### END : CONFIG #######
############################

def simulate_robot(in_robot):
    ### Keep track of data in these classes ###
    stocks_held = {}
    total_wallet = {}
    raw_wallet = {}
    raw_stock_price = {}
    smooth_stock_price_a = {}
    smooth_stock_price_b = {}

    ### While there is still stock data,   ###
    ### Get the robot to go through it and ###
    ### record the data                    ###
    while not in_robot.done():
        # Get robot to buy and sell for the day
        in_robot.simulate_day()

        # Get the current date from the stock class
        date = in_robot.get_broker().get_stock().get_date()

        # Get the amount of stocks held
        stocks_held[date] = in_robot.get_stocks_held() / STOCKS_HELD_SCALE

        # Get the wallet amount with and without stocks in them
        total_wallet[date] = in_robot.get_total_wallet() / WALLET_SCALE
        raw_wallet[date] = in_robot.get_raw_wallet() / WALLET_SCALE

        # get the raw and the stock prices
        raw_stock_price[date] = in_robot.get_stock_price()

        # Check if you should record two smooth values or just one
        if DUAL_ALGORITHM:
            smooth_stock_price_a[date] = in_robot.get_buy_smooth_stock_price()
            smooth_stock_price_b[date] = in_robot.get_sell_smooth_stock_price()
        else:
            smooth_stock_price_a[date] = in_robot.get_smooth_stock_price()

    # Plot all of the data
    pandas.Series(raw_stock_price).plot(label='Stock Price')

    if DUAL_ALGORITHM:
        pandas.Series(smooth_stock_price_a).plot(label='Smooth Stock Price [BUY]')
        pandas.Series(smooth_stock_price_b).plot(label='Smooth Stock Price [SELL]')
    else:
        pandas.Series(smooth_stock_price_a).plot(label='Smooth Stock Price')

    pandas.Series(total_wallet).plot(label='Total Wallet / ' + str(WALLET_SCALE))
    pandas.Series(raw_wallet).plot(label='Wallet / ' + str(WALLET_SCALE))
    #pandas.Series(stocks_held).plot(label='Stocks Held / ' + str(STOCKS_HELD_SCALE))

    # Show trading information
    plt.legend()
    plt.show()

### The amount that the data will be scaled on the graph
STOCKS_HELD_SCALE = 10
WALLET_SCALE = 1000

### Get the stock data into a class called my_stock ###
my_stock = HistoricalStock(ticker=TICKER, start=START)

### Simulate broker that holds all the money and my stocks ###
my_broker = Broker(stock=my_stock, wallet=START_WALLET)

### Create robot class and give it all the parameters ###
if DUAL_ALGORITHM:
    my_robot = DualTrendRobot(
        broker=my_broker, 
        buy_smoother=BUY_SMOOTH_ALGO,
        sell_smoother=SELL_SMOOTH_ALGO, 
        buy_rate=BUY_RATE, sell_rate=SELL_RATE,
        buy_margin=BUY_MARGIN, sell_margin=SELL_MARGIN
    )
else:
    my_robot = TrendRobot(
        broker=my_broker, smoother=SMOOTH_ALGO, 
        buy_rate=BUY_RATE, sell_rate=SELL_RATE,
        buy_margin=BUY_MARGIN, sell_margin=SELL_MARGIN
    )

simulate_robot(my_robot)