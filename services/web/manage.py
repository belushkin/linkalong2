import os
import redis

from flask.cli import FlaskGroup
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from rq import Worker, Queue, Connection

from app import app, db
from models import Text, Sentence
from worker import process_worker

cli = FlaskGroup(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# Changing work directory for back compatibility with Heroku
os.chdir(os.path.dirname(os.path.abspath(__file__)))


@cli.command("drop_db")
def drop_db():
    db.drop_all()
    db.session.commit()


@cli.command("db")
def create_db():
    manager.run()


@cli.command("seed_db")
def seed_db():
    text1 = Text(
        text="Hello world, Lorem Ipsum dolar sit amet, Detected new table, docker compose"
    )
    db.session.add(text1)

    text2 = Text(
        text="Hello. I am grut. No no no. Covid - 19"
    )
    db.session.add(text2)

    text3 = Text(
        text="Hello.I am grut. No no no. Covid - 20. Covidka. Covid-1984"
    )
    db.session.add(text3)

    db.session.commit()

    with Connection(redis.from_url(os.getenv('REDISTOGO_URL', app.config['REDIS_URL']))):
        q = Queue()
        q.enqueue_call(
            func=process_worker, args=(text1.id,), result_ttl=3000
        )
        q.enqueue_call(
            func=process_worker, args=(text2.id,), result_ttl=3000
        )
        q.enqueue_call(
            func=process_worker, args=(text3.id,), result_ttl=3000
        )


@cli.command("pg_trgm")
def pg_trgm():
    try:
        query = db.text("CREATE EXTENSION pg_trgm;")
        db.session.execute(query)
        db.session.commit()
    except Exception:
        pass


@cli.command("run_worker")
def run_worker():
    listen = ['default']
    redis_url = os.getenv('REDISTOGO_URL', app.config['REDIS_URL'])
    conn = redis.from_url(redis_url)

    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()


if __name__ == "__main__":
    cli()
