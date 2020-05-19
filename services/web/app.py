import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Result


@app.route("/")
def hello_world():
    return jsonify(hello="world")


if __name__ == '__main__':
    app.run()
