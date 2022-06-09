from flask import Flask, jsonify


# This is a function that will be called automatically when the app run
def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return jsonify({'message': 'Hello World!'})

    return app
