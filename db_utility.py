from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas
from av_utility import *

# ts and cc are objects to pull from the AV API for stock and crypto data
ts = init_alpha_vantage_stock()
cc = init_alpha_vantage_crypto()

Base = declarative_base()

class MarketInfo(Base):
    __tablename__ = 'MARKET_DATA'
    tag = Column(String, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)

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
    google_data = get_ticker_data(ts, 'GOOGL')

    google_most_recent = get_most_recent_stock(google_data)

    insert_into_db(google_most_recent)

    generate_plot(google_data[0]['4. close'], 'GOOGL', 'Google')

    bitcoin_data = get_cc_symbol_data(cc, 'BTC')

    bitcoin_most_recent = get_most_recent_cc(bitcoin_data)

    insert_into_db(bitcoin_most_recent)

    generate_plot(bitcoin_data[0]['4a. close (USD)'], 'BTC', 'Bitcoin')