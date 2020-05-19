import os
from flask.cli import FlaskGroup
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from models import Text, Sentence

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


if __name__ == "__main__":
    cli()
