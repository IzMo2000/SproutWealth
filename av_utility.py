#########################################################
#
# Utility for interfacing with the alphavantage API
# Written By: Izaac Molina
# Last Updated: 7/13/2023
#
# Note: The environment variable "ALPHAVANTAGE_API_KEY"
# must be set to use this functionality. This key
# allows you to access the alpha vantage API
#
# You can get an API key at:
# https://www.alphavantage.co/support/#api-key
#
#########################################################

# import libraries
import pandas
import matplotlib.pyplot as plt
import datetime
import requests
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import os


# function: calc_num_stocks
# input: investment (float) and stock price (float)
# output: the number of stocks that can be bought with the
#         current investment (int)
def calc_num_stocks(investment, stock_price):
    return (investment // stock_price)


# function: calc_num_coin
# input: investment (float) and coin price (float)
# output: the number of crypto coins that can be bought with the
#         current investment (float)
def calc_num_coin(investment, coin_price):
    return round((investment / coin_price), 4)


# function: calc_ten_yr_investment
# input: investment (float), price of stock now (float),
#        price of stock at the beginning of the month 10
#        years ago (float)
# output: investment worth after 10 years (float)
def calc_ten_yr_investment(investment, price_now, price_in_past):
    num_stocks = calc_num_stocks(investment, price_in_past)

    return round((num_stocks * price_now), 2)


# function: generate_plot
# input: pandas dataframe containing stock/coin data, ticker/symbol name
#        for stock/coin(str), full name for stock/coin (str)
# output: saves plot of recent stock history as a .png in the "statc" folder
def generate_plot(data, ticker, full_name):

    # plot data using matplotlib
    data.plot()
    plt.title(f'{full_name} ({ticker}) stock history (15 min)')

    # save plot into static folder
    image_path = f"/home/IzMo2000/SproutWealth/static/{ticker}_plot.png"
    plt.savefig(image_path, format='png')

    # indicate success
    return True


# function: get_cc_symbol_data
# input: object to access alpha vantage crypto data, symbol for coin to
#        find data on
# output: returns pandas data frame of cryptocurrency data
def get_cc_symbol_data(cc, symbol):
    return cc.get_digital_currency_daily(symbol=symbol, market='CNY')


# function: get_first_av_row
# input: pandas data taken from AV api
# output: returns data from first row of pandas dataframe
def get_first_av_row(data):
    # just grab the dataframe, not the metadata
    data_frame = data[0]

    # return the first line data of the dataframe
    return data_frame.head(1)


# function: get_most_recent_cc
# input: pandas crypto data
# output: returns dictionary of the most recent crypto info
def get_most_recent_cc(data):
    first_row = get_first_av_row(data)
    dict_result = {
        'tag': data[1]['2. Digital Currency Code'],
        'open': float(first_row['1b. open (USD)'].item()),
        'high': float(first_row['2b. high (USD)'].item()),
        'low': float(first_row['3b. low (USD)'].item()),
        'close': float(first_row['4b. close (USD)'].item())
    }

    return dict_result


# function: get_most_recent_stock
# input: pandas stock data
# output: returns dictionary of the most recent stock info
def get_most_recent_stock(data):

    # grab most recent data in intraday data set
    first_row = get_first_av_row(data)

    # convert data to dictionary and return
    dict_result = {
        'tag': data[1]['2. Symbol'],
        'open': float(first_row['1. open'].item()),
        'high': float(first_row['2. high'].item()),
        'low': float(first_row['3. low'].item()),
        'close': float(first_row['4. close'].item())
    }

    return dict_result


# function: get_ten_year_price
# input: ticker for stock (str)
# output: returns price of stock for given ticker
def get_ten_year_price(ticker):

    # find the current month
    curr_month = str(datetime.now().month).zfill(2)

    # determine year that was ten years ago
    ten_years_ago = str(datetime.now().year - 10)

    # grab ten year price from API using a get request,
    # convert called data to json
    url = (
        'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&'
        f'symbol={ticker}&interval=5min&month={ten_years_ago}-{curr_month}'
        '&outputsize=full&apikey=I0C349XI5KUR4NUR'
    )

    r = requests.get(url)
    data = r.json()["Time Series (5min)"]

    # get the data point at the beginning of the month
    first_date_in_month = list(data)[-1]

    # return the price ten years ago at the beginning of the month
    return float(data[first_date_in_month]['4. close'])


# function: get_ticker_data
# input: object for grabbing stock data from AV api, ticker for stock (str)
# output: returns pandas data of given ticker
def get_ticker_data(ts, ticker):
    return ts.get_intraday(ticker)


# function: init_alpha_vantage_crypto
# input: none
# output: returns data object to access crypto data from alphavantage
def init_alpha_vantage_crypto():
    return CryptoCurrencies(output_format='pandas')


# function: init_alpha_vantage_stock
# input: none
# output: returns data object to access stock data from alphavantage
def init_alpha_vantage_stock():
    return TimeSeries(output_format='pandas')
