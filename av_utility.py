import pandas
import matplotlib.pyplot as plt
import datetime
import requests
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies

def calc_num_stocks(investment, stock_price):
    return (investment // stock_price)

def calc_num_coin(investment, coin_price):
    return round((investment / coin_price), 4)

def calc_ten_yr_investment(investment, price_now, price_in_past):
    num_stocks = calc_num_stocks(investment, price_in_past)

    return round((num_stocks * price_now), 2)

def generate_plot(data, ticker, full_name):
    data.plot()
    plt.title(f'{full_name} ({ticker}) stock history (15 min)')
    plt.show()
    image_path = f"static/{ticker}_plot.png"
    plt.savefig(image_path, format='png')

    return True

def get_cc_symbol_data(cc, symbol):
    return cc.get_digital_currency_daily(symbol=symbol, market='USD')

def get_first_av_row(data):
    data_frame = data[0]

    return data_frame.head(1)

def get_most_recent_cc(data):
    first_row = get_first_av_row(data)
    dict_result = {
        'tag': data[1]['2. Digital Currency Code'],
        'open': float(first_row['1a. open (USD)'].item()),
        'high': float(first_row['2a. high (USD)'].item()),
        'low': float(first_row['3a. low (USD)'].item()),
        'close': float(first_row['4a. close (USD)'].item())
    }

    return dict_result

def get_most_recent_stock(data):

    # grab most recent data in intraday data set
    first_row = get_first_av_row(data)

    dict_result = {
        'tag': data[1]['2. Symbol'],
        'open': float(first_row['1. open'].item()),
        'high': float(first_row['2. high'].item()),
        'low': float(first_row['3. low'].item()),
        'close': float(first_row['4. close'].item())
    }

    return dict_result

def get_ten_year_price(ticker):
    curr_month = str(datetime.now().month).zfill(2)
    curr_day = str(datetime.now().day).zfill(2)
    ten_years_ago = str(datetime.now().year - 10)


    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&month={ten_years_ago}-{curr_month}&outputsize=full&apikey=I0C349XI5KUR4NUR'
    r = requests.get(url)
    data = r.json()["Time Series (5min)"]

    first_date_in_month = list(data)[-1]

    return float(data[first_date_in_month]['4. close'])
    

def get_ticker_data(ts, ticker):
    return ts.get_intraday(ticker)

def init_alpha_vantage_crypto():
    return CryptoCurrencies(key='I0C349XI5KUR4NUR', output_format='pandas')

def init_alpha_vantage_stock():
    return TimeSeries(key='I0C349XI5KUR4NUR', output_format='pandas')