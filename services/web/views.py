import os
import config
import redis

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from rq import Worker, Queue, Connection
from rq.job import Job

from app import app, db
from worker import process_worker
from models import Text, Sentence


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
    """
    Route for adding new texts to the database
    It stores the text itself and sends id of the stored text for further processing in the redis queue
    :return: JSON {text=1} where 1 is id of the stored text
    """

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


@app.route("/list/<text_id>", methods=['GET'])
def list_text(text_id):
    """
    Method for getting all stored sentences of the stored text
    It receives text_id, fetch the database and return JSON of the all sentences in the text
    :param text_id: Int field represents stored text id
    :return:
        {
          "id": 1,
          "sentences": [
            "Hello.",
            "I am grut.",
            "No no no.",
            "Covid-19.",
            "Covid18"
          ],
          "text": "Hello. I am grut. No no no. Covid-19. Covid18"
        }
    """
    listed_text = Text.query.filter_by(id=text_id).first()

    if not listed_text:
        raise Exception(f"There is no such text with id={text_id} stored in the database")

    sentences = Sentence.query.filter_by(parent_id=listed_text.id).all()

    result = {'text': listed_text.text, 'id': listed_text.id, 'sentences': []}

    for value in sentences:
        result['sentences'].append(value.sentence)

    return jsonify(result)


@app.route("/list", methods=['GET'])
def list_all_texts():
    """
    Route lists all texts stored in the database
    :return:
    [
      {
        "id": 1,
        "text": "Hello. I am grut. No no no. Covid-19. Covid18"
      }
    ]
    """

    texts = Text.query.all()

    result = [{'id': value.id, 'text': value.text} for value in texts]

    return jsonify(result)
