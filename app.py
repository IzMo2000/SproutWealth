from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import git
from search_form import InvestmentForm
from alpha_vantage.timeseries import TimeSeries

ts = TimeSeries(key='I0C349XI5KUR4NUR')
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_intraday('GOOGL')

most_recent_data = data[list(data.keys())[0]]

print(most_recent_data)


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
    investment = InvestmentForm()

    # check form data
    if investment.validate_on_submit():


        return redirect(url_for('search_result'))

    # return basic home template
    return render_template('home.html', form=investment)


# define search result page
@app.route("/result", methods=['GET'])
def search_result():


    return render_template('result.html', stock_open=most_recent_data['1. open'], stock_high=most_recent_data['2. high'], 
                           stock_low=most_recent_data['3. low'],stock_close=most_recent_data['4. close'])


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