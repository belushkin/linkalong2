docker-compose exec web python manage.py db init
docker-compose exec web python manage.py db migrate

docker-compose exec db psql --username=flask --dbname=flask_dev

heroku config --app linkalong-stage
heroku addons:create heroku-postgresql:hobby-dev --app linkalong-stage


