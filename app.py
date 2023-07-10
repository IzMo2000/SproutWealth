from flask import Flask, render_template, url_for, flash, redirect, request
import git
import search_form

# initialize flask app
app = Flask(__name__)


# define home page
@app.route("/", methods=['GET'])
def home_page():
    # get form data
    investment = InvestmentForm()

    # check form data
    if investment.validate_on_submit():
        return redirect(url_for('search_result'))

    # gonna need to add some parameters here....
    return render_template('[INSERT HOME PAGE HTML NAME]')


# define search result apge
@app.route("/result", methods=['GET', 'POST'])
def search_result():

    return render_template('[INSERT SEARCH HTML NAME]')


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
     