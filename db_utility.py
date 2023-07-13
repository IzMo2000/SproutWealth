from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
import pandas
from av_utility import *

# ts and cc are objects to pull from the AV API for stock and crypto data
ts = init_alpha_vantage_stock()
cc = init_alpha_vantage_crypto()

last_updated = ""

Base = declarative_base()

class MarketInfo(Base):
    __tablename__ = 'MARKET_DATA'
    tag = Column(String, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)

def check_for_db_update():
    global last_updated

    todays_date = date.today()

    if todays_date != last_updated:
        update_db()
        last_updated = todays_date

def init_db():
    engine = create_engine('sqlite:///aplha_vantage.db')

    Session = sessionmaker(bind=engine)
    session = Session()
    
    Base.metadata.create_all(engine)

    session.close()


def insert_into_db(data):
    engine = create_engine('sqlite:///aplha_vantage.db')
    
    Session = sessionmaker(bind=engine)
    session = Session()

    tag = data['tag']
    existing_market_info = session.query(MarketInfo).filter_by(tag=tag).first()

    if existing_market_info:
        for key, value in data.items():
            setattr(existing_market_info, key, value)
        session.merge(existing_market_info)

    else:
        market_info = MarketInfo(**data)
        session.add(market_info)
    
    all_market_info = session.query(MarketInfo).all()

    print(all_market_info)

    session.commit()
    session.close()


def get_market_data_from_db(tag):
    engine = create_engine('sqlite:///aplha_vantage.db')
    
    Session = sessionmaker(bind=engine)
    session = Session()

    tag_info = session.query(MarketInfo).filter_by(tag=tag).first()
    session.close()

    market_data = {
        'tag': tag_info.tag,
        'open': tag_info.open,
        'high': tag_info.high,
        'low': tag_info.low,
        'close': tag_info.close
    }

    return market_data

def update_db():
    stocks = ['GOOGL', 'WFC']
    ccs = ['BTC', 'ETH']

    for ticker in stocks:
        current_data = get_ticker_data(ts, ticker)

        most_recent_data = get_most_recent_stock(current_data)

        insert_into_db(most_recent_data)

        if ticker == 'GOOGL':
            generate_plot(current_data[0]['4. close'], 'GOOGL', 'Google')
    
    for coin in ccs:
        current_data = get_cc_symbol_data(cc, coin)
        
        most_recent_data = get_most_recent_cc(current_data)

        insert_into_db(most_recent_data)

        if coin == 'BTC':
            generate_plot(current_data[0]['4a. close (USD)'], 'BTC', 'Bitcoin')