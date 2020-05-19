from app import db
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Text(db.Model):
    __tablename__ = 'texts'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    children = relationship("Sentence")

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'<id {self.id}>'


class Sentence(db.Model):
    __tablename__ = 'sentences'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('texts.id'))
    sentence = db.Column(db.String())

    def __init__(self, parent_id, sentence):
        self.parent_id = parent_id
        self.sentence = sentence

    def __repr__(self):
        return f'<id {self.id}>'
