from models import Text, Sentence
from app import app, db
from utils.splitter import split


def process_worker(textId):

    if not textId:
        raise Exception("There is nothing to extract, please add text id to the message")

    # Getting the result from the DB
    result = Text.query.filter_by(id=textId).first()

    if not result:
        raise Exception("There is no such text stored in the database")

    # Split text on sentences
    sentences = split(result.text)

    # Store sentences in the database
    for sentenceFromTheList in sentences:
        sent = Sentence(
            parent_id=result.id,
            sentence=sentenceFromTheList
        )
        db.session.add(sent)
        db.session.commit()
