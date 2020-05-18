import os
from flask import Flask, jsonify
# from .config import DevelopmentConfig


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


@app.route("/")
def hello_world():
    return jsonify(hello="world")


if __name__ == '__main__':
    app.run()
