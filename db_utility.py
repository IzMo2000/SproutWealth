#########################################################
###
### Utility for managing stock and crypto data from alpha
### vantage API using a SQL database
### Written By: Izaac Molina
### Last Updated: 7/13/2023
###
#########################################################

from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
import pandas
from av_utility import *

# ts and cc are objects to pull from the AV API for stock and crypto data
ts = init_alpha_vantage_stock()
cc = init_alpha_vantage_crypto()

# define the last day the database was updated
last_updated = ""

# set up base to use for creating rows in database
Base = declarative_base()


# define class for data to be stored in database
class MarketInfo(Base):
    __tablename__ = 'MARKET_DATA'
    tag = Column(String, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)


# function: check_for_db_update
# input: none
# output: checks if the databse must be updated, if so, updates it
def check_for_db_update():
    # set last_updated to global version so it can be updated
    global last_updated

    # find today's date
    todays_date = date.today()

    # check if data base has been updated today, if not, update it
    if todays_date != last_updated:
        update_db()
        last_updated = todays_date


# function: check_for_db_update
# input: none
# output: initializes SQL database
def init_db():
    # start session
    session, engine = start_db_session()
    
    # create database
    Base.metadata.create_all(engine)

    # end session
    session.close()


# function: check_for_db_update
# input: data to be inserted into table (dict)
# output: data inserted into database
def insert_into_db(data):
    # start session
    session, engine = start_db_session()

    # get tag from data to be inserted
    tag = data['tag']

    # check if data with this tag already exists
    existing_market_info = session.query(MarketInfo).filter_by(tag=tag).first()

    # if data exists, replace it
    if existing_market_info:
        for key, value in data.items():
            setattr(existing_market_info, key, value)
        session.merge(existing_market_info)

    # data doesnt exist, add it
    else:
        market_info = MarketInfo(**data)
        session.add(market_info)

    # commit and end session
    session.commit()
    session.close()


# function: get_market_data_from_db
# input: tag to use for retrieval, typically a ticker or coin symbol ('str')
# output: data coresponding to the given tag from the database (dict)
def get_market_data_from_db(tag):
    # start session
    session, engine = start_db_session()

    # query database for desired tag data
    tag_info = session.query(MarketInfo).filter_by(tag=tag).first()

    # end session
    session.close()

    # package data into a dictionary and return
    market_data = {
        'tag': tag_info.tag,
        'open': tag_info.open,
        'high': tag_info.high,
        'low': tag_info.low,
        'close': tag_info.close
    }

    return market_data


# function: start_db_session
# input: none
# output: the database engine, and current session for editing
def start_db_session():
    engine = create_engine('sqlite:///aplha_vantage.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine


# function: update_db
# input: none
# output: updates the database with the most recent market data
def update_db():
    stocks = ['GOOGL', 'WFC']
    ccs = ['BTC', 'ETH']

    # upload all stock data
    for ticker in stocks:
        current_data = get_ticker_data(ts, ticker)

        most_recent_data = get_most_recent_stock(current_data)

        insert_into_db(most_recent_data)

        if ticker == 'GOOGL':
            generate_plot(current_data[0]['4. close'], 'GOOGL', 'Google')
    
    # upload all crypto data
    for coin in ccs:
        current_data = get_cc_symbol_data(cc, coin)
        
        most_recent_data = get_most_recent_cc(current_data)

        insert_into_db(most_recent_data)

        if coin == 'BTC':
            generate_plot(current_data[0]['4b. close (USD)'], 'BTC', 'Bitcoin')