from flask import Flask
import git

# initialize flask app
app = Flask(__name__)

# define home page
@app.route("/")                          
def hello_world():
    return "<p>Hello, World!</p>" 

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