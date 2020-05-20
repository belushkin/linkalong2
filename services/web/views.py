import os
import config
import redis

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from rq import Worker, Queue, Connection
from rq.job import Job

from app import app, db
from worker import process_worker
from models import Text


@app.route("/")
def hello_world():
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


@app.route("/text", methods=['POST'])
def add_text():
    if request.is_json:
        content = request.get_json()
        if content['text']:
            # Store newly added text to the database
            text = Text(
                text=content['text'].strip()
            )
            db.session.add(text)
            db.session.commit()

            # Push extraction job to the queue
            with Connection(redis.from_url(os.getenv('REDISTOGO_URL', 'redis://redis:6379'))):
                q = Queue()
                job = q.enqueue_call(
                    func=process_worker, args=(text.id,), result_ttl=3000
                )

            return jsonify(text=text.id)
        else:
            raise Exception("Please add text variable to the json")
    else:
        raise Exception("Please add content-type application/json to the request")

    # with Connection(redis.from_url(os.getenv('REDISTOGO_URL', 'redis://redis:6379'))):
    #     q = Queue()
    #     job = q.fetch_job(job_key)
    #
    #     if job.is_finished:
    #         return str(job.result), 200
    #     else:
    #         return "Nay!", 202
