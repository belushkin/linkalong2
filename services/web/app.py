import os
import config
import redis

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from rq import Worker, Queue, Connection
from rq.job import Job

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import *
from views import hello_world, get_results, add_text


if __name__ == '__main__':
    app.run()
