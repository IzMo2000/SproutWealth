from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import git
import threading
from search_form import *
from av_utility import *
from db_utility import *

todays_date = date.today()
last_updated = ""

# initialize the database
init_db()

# initialize flask app
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'f9fc1ee355f6b6051ed273eef250d483'

# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aplha_vantage.db'
db = SQLAlchemy(app)


# define home page
@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def home_page():
    # get form data
    form = InvestmentForm()

    # check form data
    if form.validate_on_submit():
        investment = form.investment.data
        return redirect(url_for('search_result', investment = investment))

    # return basic home template
    return render_template('home.html', form=form)


# define search result page
@app.route("/result", methods=['GET'])
def search_result():
    global last_updated
    global todays_date

    if 'investment' in request.args:

        todays_date = date.today()

        if last_updated != todays_date:
            update_db()
            google_price_ten_years_ago = get_ten_year_price('GOOGL')

        investment = float(request.args.get('investment', 0))

        google_most_recent = get_market_data_from_db('GOOGL')

        num_stocks = calc_num_stocks(investment, google_most_recent['open'])

        ten_year_investement = calc_ten_yr_investment(investment, google_most_recent['open'], google_price_ten_years_ago)
        
        print(google_most_recent)
        print(num_stocks)
        print(ten_year_investement)

        return render_template('result.html', stock_open=google_most_recent['open'], stock_high=google_most_recent['high'], 
                               stock_low=google_most_recent['low'], stock_close=google_most_recent['close'])
    else:
        return redirect(url_for('home_page'))


# define route to update_server, connecting git repo to PythonAnywhere
@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/IzMo2000/SproutWealth')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


# start server

if __name__ == '__main__':               
    app.run(debug=True, host="0.0.0.0")        