docker-compose exec web python manage.py db init
docker-compose exec web python manage.py db migrate
docker-compose exec web python manage.py db heads
docker-compose exec web python manage.py db current

docker-compose exec db psql --username=flask --dbname=flask_dev

heroku config --app linkalong-stage
heroku addons:create heroku-postgresql:hobby-dev --app linkalong-stage


heroku run python services/web/manage.py db init --app linkalong-stage
heroku run python services/web/manage.py db upgrade --app linkalong-stage



