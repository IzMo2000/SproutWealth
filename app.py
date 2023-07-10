from flask import Flask
import git

# initialize flask app
app = Flask(__name__)

# define home page
@app.route("/")                          
def hello_world():
    return "<p>Hello, World!</p>" 

# start server
if __name__ == '__main__':               
    app.run(debug=True, host="0.0.0.0")       