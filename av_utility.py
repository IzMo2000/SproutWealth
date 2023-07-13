import pandas
import matplotlib.pyplot as plt
import datetime
import requests
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries

def calc_num_stocks(investment, stock_price):
    return (investment // stock_price)

def calc_ten_yr_investment(investment, price_now, price_in_past):
    num_stocks = calc_num_stocks(investment, price_in_past)

    return round((num_stocks * price_now), 2)

def generate_plot(data, ticker):
    data[0]['4. close'].plot()
    plt.title(f'{ticker} stock history (15 min)')
    plt.show()
    image_path = f"static/{ticker}_plot.png"
    plt.savefig(image_path, format='png')

    return True

def get_most_recent(data):

    # grab most recent data in intraday data set
    data_frame = data[0]

    first_row = data_frame.head(1)

    dict_result = {
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
    data = r.json()['Time Series (5min)']

    first_date_in_month = list(data)[-1]

    return float(data[first_date_in_month]['4. close'])
    

def get_ticker_data(ts, ticker):
    return ts.get_intraday(ticker)

def init_alpha_vantage():
    return TimeSeries(key='I0C349XI5KUR4NUR', output_format='pandas')