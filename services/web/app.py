import os
from flask import Flask, jsonify

import config

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route("/")
def hello_world():
    return jsonify(hello="world")


if __name__ == '__main__':
    app.run()
