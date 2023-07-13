from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import git
import threading
from search_form import *
from av_utility import *
from db_utility import *

# initialize the database
init_db()

# initialize flask app
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'f9fc1ee355f6b6051ed273eef250d483'


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

    if 'investment' in request.args:

        check_for_db_update()

        investment = round(float(request.args.get('investment', 0)), 2)

        google_data = get_market_data_from_db('GOOGL')
        google_data['num_stocks'] = calc_num_stocks(investment, google_data['open'])

        wells_data = get_market_data_from_db('WFC')
        wells_data['num_stocks'] = calc_num_stocks(investment, wells_data['open'])

        bitcoin_data = get_market_data_from_db('BTC')
        bitcoin_data['num_coins'] = calc_num_coin(investment, bitcoin_data['open'])

        ethereum_data = get_market_data_from_db('ETH')
        ethereum_data['num_coins'] = calc_num_coin(investment, ethereum_data['open'])

        google_price_ten_years_ago = get_ten_year_price('GOOGL')

        ten_year_investment = calc_ten_yr_investment(investment, google_data['open'], google_price_ten_years_ago)
        
        return render_template('result.html', google = google_data, wells = wells_data, bitcoin = bitcoin_data, ethereum = ethereum_data, 
                               user_investment=investment, ten_year_investment = ten_year_investment)
    else:
        return redirect(url_for('home_page'))
      

@app.route("/resources", methods=['GET'])
def resource_page():
    return render_template('resources.html')

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