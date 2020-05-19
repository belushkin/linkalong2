import os

from flask.cli import FlaskGroup

import redis
from app import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models import Sentence, Text
from rq import Connection, Queue, Worker

cli = FlaskGroup(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# Changing work directory for back compatibility with Heroku
os.chdir(os.path.dirname(os.path.abspath(__file__)))


@cli.command("db")
def create_db():
    manager.run()


@cli.command("seed_db")
def seed_db():
    db.session.add(Text(text="Hello world, Lorem Ipsum dolar sit amet, Detected new table, docker compose"))
    db.session.commit()


@cli.command("run_worker")
def run_worker():
    listen = ['default']
    redis_url = os.getenv('REDISTOGO_URL', 'redis://redis:6379')
    conn = redis.from_url(redis_url)

    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()


if __name__ == "__main__":
    cli()
