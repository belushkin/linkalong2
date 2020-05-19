import os
from flask.cli import FlaskGroup
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

cli = FlaskGroup(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

@cli.command("db")
def create_db():
    manager.run()

#     # db.drop_all()
#     # db.create_all()
#     # db.session.commit()


if __name__ == "__main__":
    cli()
