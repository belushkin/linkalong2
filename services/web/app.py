import os
import config

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from rq import Queue
from rq.job import Job

from worker import conn

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

q = Queue(connection=conn)

from models import *


def process_worker(url):

    print(url)
    return jsonify(hello="mesama")


@app.route("/")
def hello_world():
    from app import process_worker

    job = q.enqueue_call(
        func=process_worker, args=("test",), result_ttl=1000
    )

    return jsonify(job_id=job.get_id())


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        print((job.result))
        return str(job.result), 200
    else:
        return "Nay!", 202


if __name__ == '__main__':
    app.run()
