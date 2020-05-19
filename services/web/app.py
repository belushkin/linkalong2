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


def process_worker(url):

    print(url)
    return jsonify(hello="mesama")


@app.route("/")
def hello_world():
    from app import process_worker

    with Connection(redis.from_url(os.getenv('REDISTOGO_URL', 'redis://redis:6379'))):
        q = Queue()
        job = q.enqueue_call(
            func=process_worker, args=("test",), result_ttl=1000
        )

    return jsonify(job_id=job.get_id())


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    with Connection(redis.from_url(os.getenv('REDISTOGO_URL', 'redis://redis:6379'))):
        q = Queue()
        job = q.fetch_job(job_key)

        if job.is_finished:
            return str(job.result), 200
        else:
            return "Nay!", 202


if __name__ == '__main__':
    app.run()
