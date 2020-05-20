docker-compose exec web python manage.py db init
docker-compose exec web python manage.py db migrate
docker-compose exec web python manage.py db heads
docker-compose exec web python manage.py db current


docker-compose exec web python manage.py pg_trgm

# custom commands
docker-compose exec web python manage.py seed_db


docker-compose exec web python manage.py db revision --autogenerate -m "Added Text and Sentence models"

# Connect to the database
docker-compose exec db psql --username=flask --dbname=flask_dev

heroku config --app linkalong-stage
heroku addons:create heroku-postgresql:hobby-dev --app linkalong-stage


heroku run python services/web/manage.py db init --app linkalong-stage
heroku run python services/web/manage.py db upgrade --app linkalong-stage

heroku logs --tail --remote stage

For staging: git push stage master
For production: git push pro master



docker-compose exec web python -m pytest