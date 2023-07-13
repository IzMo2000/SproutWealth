from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.blocking import BlockingScheduler
import git
import threading
from search_form import *
from av_utility import *

google_data, metadata, google_most_recent = None, None, None
google_price_ten_years_ago = None

ts = init_alpha_vantage()

# update alpha vantage data
def update_alpha_vantage():
    global google_data
    global google_most_recent
    global google_price_ten_years_ago

    google_data = get_ticker_data(ts, 'GOOGL')

    google_most_recent = get_most_recent(google_data)

    generate_plot(google_data, 'GOOGL')

    google_price_ten_years_ago = get_ten_year_price('GOOGL')

# initializes alpha vantage databse
update_alpha_vantage()

# sets the database to update at midnight
scheduler = BlockingScheduler()
scheduler.add_job(update_alpha_vantage, 'cron', hour=0)

# Create a separate thread for the scheduler
scheduler_thread = threading.Thread(target=scheduler.start)

# Start the scheduler thread
scheduler_thread.start()


# initialize flask app
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'f9fc1ee355f6b6051ed273eef250d483'

# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aplha_vantage.db'
db = SQLAlchemy(app)

# From Codio Work: Model for adding data to database from form 
#                  (Not sure if we have to do that, though)
# class (db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   username = db.Column(db.String(20), unique=True, nullable=False)
#   email = db.Column(db.String(120), unique=True, nullable=False)
#   password = db.Column(db.String(60), nullable=False)

#   def __repr__(self):
#     return f"User('{self.username}', '{self.email}')"

#   with app.app_context():
#     db.create_all()


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
        investment = float(request.args.get('investment', 0))

        google_price_now = google_most_recent['open']

        num_stocks = calc_num_stocks(investment, google_price_now)

        ten_year_investement = calc_ten_yr_investment(investment, google_price_now, google_price_ten_years_ago)

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