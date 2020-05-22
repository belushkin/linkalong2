# Linkalong second tech assessment

## Description of the task

Single page application must be developed using Flask python framework on the backend and your favorite UI framework on the frontend.
Application should allow user to add text up 1 mb size. After text has been added it must be decoupled on the sentences. 
User must see a list of added texts to the application and can browse these texts (each text has unique link). On the text page
user sees list of sentences of this text. Sentences are clickable and user can click on each sentence and see the result of the search
by selected sentence against all stored sentences from previous stored texts altogether with similarity metrics sorted by similarity.
Most similar sentences from different texts come first and less similar sentences come next.


#### Splitting given task into stories and putting estimations before coding
| Task description  | Given estimate | Real estimate |
| ------------- | ------------- | ------------- |
| Investigating Flask  | -  | -  |
| Investigating Heroku  | -  | -  |
| Investigating Docker and Docker Compose  | -  | -  |
| Reading technical task and deciding about MVP  | -  | -  |
| Investigating similarity best practics  | -  | -  |
| Creating Dockerfile and compose files  | -  | -  |
| Setup Heroku account and download CLI client  | -  | -  |
| Creating First API endpoints | -  | -  |
| Create DB schema  | -  | -  |
| Create Models  | -  | -  |
| Writing tests  | -  | -  |
| Adding UI framework  | -  | -  |
| Add Reverse Proxy  | -  | -  |
| Integrate and test app  | -  | -  |
| **Total**  | **16h**  | **36h**  |

### Technical details regarding task for further learning and for fellows who might need such apps

Structure of the application is designed to be able easily be deployed to Heroku from the github. That's why there are 2 
`requirements.txt` files in the app.

App has 3 stages:
- dev (considered to be Docker containers)
- stage (Heroku with gunicorn and redis and builded Javascript, without Nginx)
- prod (Final stage with all tested files and battle ready Javascript)

`Heroku` part is not completely tested and prepared but I might spend another 1 or 2 days to polish the code in order to be able
to deploy the app there.

App has 1 reverse proxy `Nginx` which proxies requests from the browser to internal services:
- web (backend)
- client (frontend)

#### Backend description

Backend part implemented using `Flask`.
Things to improve:
- Add error handling
- Use blueprints
- Move views, models, worker to folders in order not to have everything in 1 root folder

App use Postgres SQL as a main storage engine for preserving decoupled sentences and implement Trigram search mechanism
through the `pg_trgm` extension.

`SQLAlchemy` database toolkit is used for database operations plus `Alembic` database migration tool.

For effective sentence splitting App use `Redis` and `RQ` queue small app. Workers itself uses `nltk_data` package for text 
processing. For performance I stored only English tokenizers.

`Pytest` is included and can be launched.

#### Frontend description

Frontend implemented using `Next.js` `React` framework: https://nextjs.org/

I decided to use it since it is pretty easy to setup and start using the app. As well as I spent 24 hours on Python
and 8 hours on UI I can say next:

I tried to implement latest features from React which incapsulated inside next.js and I think it works pretty nice.
For CSS I used `TailwindCSS` and some vanilla CSS.

In UI part there are 2 ways of Ajax queries:
- Query to internal network (server side rendering) where I use container name
- Query to public network (client side rendering)  where I use localhost or 0.0.0.0

UI part itself is pretty basic, no fancy features and nice styles. As well it is in the development mode from where
we come to the next part of this explanation.

What can be improved:
- Adding PROD mode to Next.js for Javascript compiling and moving to the next stage mode of whole Application
- Polishing CSS
- Adding pagering (involve backend as well) to the main page
- Adding tests to the UI side
- Adding environment variables and moving domain names from the code there


### Final words
In general I enjoyed this task. Most impressive part as for me was Python task especially with Trigram search and UI
part I found also interesting but less complex.

Thank you for this experience.


### Technologies used in the assessment
- Python 3.8
- Docker
- Docker Compose
- Flask
- Redis
- Bash
- Git
- TailwindCSS
- React
- Next.js
- Postges SQL
- Alembic
- SQL Alchemy
- RQ
- Heroku
- Nginx + gunicorn
- NodeJS


### Prerequisites
Docker.io and docker-compose must be installed in the system in order to be able to use the app.
OS Linux

## How to setup the application:
```bash
git clone https://github.com/belushkin/linkalong2.git
cd linkalong2; ./toolbox.sh up
```

## How to run tests
```bash
docker-compose exec web python -m pytest
```

## URL of the running app
http://0.0.0.0:8080/

## Basic script usage:
Application has **toolbox.sh** script. It is very easy run, stop, ssh, rebuild, run tests and stop the application.

```bash
./toolbox.sh up # run the application
./toolbox.sh rebuild # rebuild the image
./toolbox.sh ssh # ssh to the container
./toolbox.sh tests # run tests (might not be working)
./toolbox.sh down # stop the application
```

### Technical help for those who will launch this app

#### Commands for operating database an run cli commands of flask cli
```bash
docker-compose exec web python manage.py db init
docker-compose exec web python manage.py db migrate
docker-compose exec web python manage.py db heads
docker-compose exec web python manage.py db current
docker-compose exec web python manage.py pg_trgm
docker-compose exec web python manage.py seed_db
```

#### Alembic
```bash
docker-compose exec web python manage.py db revision --autogenerate -m "Added Text and Sentence models"
```

#### Postgres
```bash
docker-compose exec db psql --username=flask --dbname=flask_dev
```

#### Heroku
```bash
heroku config --app linkalong-stage
heroku addons:create heroku-postgresql:hobby-dev --app linkalong-stage
heroku run python services/web/manage.py db init --app linkalong-stage
heroku run python services/web/manage.py db upgrade --app linkalong-stage
heroku logs --tail --remote stage
```

#### Heroku git
```bash
For staging: git push stage master
For production: git push pro master
```

#### Tests
```bash
docker-compose exec web python -m pytest
```

#### Next.js
```bash
npx tailwind init
```

#### Docker
```bash
docker exec -it 1f90af2b50e8 /bin/sh
```

## Contributors
@belushkin

## License
MIT License