import os
import config
import redis
from app import app

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from rq import Worker, Queue, Connection
from rq.job import Job


# from app import app

# from app import process_worker

@app.route("/")
def hello_world():
    return jsonify(job_id="anus")

    # with Connection(redis.from_url(os.getenv('REDISTOGO_URL', 'redis://redis:6379'))):
    #     q = Queue()
    #     job = q.enqueue_call(
    #         func=process_worker, args=("test",), result_ttl=1000
    #     )

    # return jsonify(job_id=job.get_id())


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    with Connection(redis.from_url(os.getenv('REDISTOGO_URL', 'redis://redis:6379'))):
        q = Queue()
        job = q.fetch_job(job_key)

        if job.is_finished:
            return str(job.result), 200
        else:
            return "Nay!", 202
