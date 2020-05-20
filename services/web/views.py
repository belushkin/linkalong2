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


@app.route("/api")
def hello_world():
    return jsonify(job_id="anasse")


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    with Connection(redis.from_url(os.getenv('REDISTOGO_URL', app.config['REDIS_URL']))):
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
            with Connection(redis.from_url(os.getenv('REDISTOGO_URL', app.config['REDIS_URL']))):
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
        {
          "id": 1,
          "value": "Hello."
        }
      ],
      "text": "Hello. I am grut. No no no. Covidka. Covid20"
    }
    """
    listed_text = Text.query.filter_by(id=text_id).first()

    if not listed_text:
        raise Exception(f"There is no such text with id={text_id} stored in the database")

    sentences = Sentence.query.filter_by(parent_id=listed_text.id).all()

    result = {'text': listed_text.text, 'id': listed_text.id, 'sentences': []}

    for value in sentences:
        result['sentences'].append({'value': value.sentence, 'id': value.id})

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


@app.route("/search/<sentence_id>", methods=['GET'])
def search_similar_texts(sentence_id):
    """
    Route search similar texts based on the Trigram (or Trigraph) Concepts
    :return:
    [
      {
        "sentence_id": 5,
        "sim": 1.0,
        "text": "Covid - 19",
        "text_id": 2
      }
    ]
    """

    original_sentence = Sentence.query.filter_by(id=sentence_id).first()
    if not original_sentence:
        raise Exception("There is no such sentence in the database")

    query = db.text(f"select * from (select parent_id, id, sentence, similarity('{original_sentence.sentence}', "
                    f"sentence) as sim from sentences) as t WHERE sim > 0 order by sim desc;")
    resultset = db.session.execute(query).fetchall()

    result = []
    for row in resultset:
        result.append({'text_id': row[0], 'sentence_id': row[1], 'text': row[2], 'sim': row[3]})

    return jsonify(result)
