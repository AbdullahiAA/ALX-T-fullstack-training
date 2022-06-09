from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello Abdullah!"


# Method One of running a flask server (Terminal)
# FLASK_APP=03_flask_hello.py FLASK_DEBUG=true flask run


# Method Two of running a flask server (From the file)
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
