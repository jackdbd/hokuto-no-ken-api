# Hokuto Flask

Hokuto no Ken [REST API](https://floating-headland-89373.herokuapp.com/api/v1/), powered by [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/).

Data from the [Hokuto Renkitōza](http://hokuto.wikia.com/wiki/Main_Page) wiki.


## Installation

If you want just the API:

```sh
pipenv install
```

Otherwise, if you want to be able to test the code and use the code formatter:

```sh
pipenv install --dev
```


## Usage

```sh
pipenv run flask run

# OR
pipenv --venv  # to know the name of YOUR-VIRTUALENV
workon YOUR-VIRTUALENV
flask run
```


## Migrations

```sh
# Init the migrations repository (only once)
pipenv run flask db init

# Create the migration script (every time there is a change in the schema)
pipenv run flask db migrate

# Run all migration scripts (i.e migrate the database to the latest revision)
pipenv run flask db upgrade
```


## Tests

```sh
# Activate your virtual environment (you can use pipenv --venv to know the name
# of YOUR-VIRTUALENV)
workon YOUR-VIRTUALENV

# Instead of setting FLASK_ENV=test in the .env file, you can assign
# the FLASK_ENV environment variable on-the-fly and run the tests.
# This is handy when running the tests locally.
env FLASK_ENV='test' pytest -v
```


## Run gunicorn locally

It might be useful to try running the application with gunicorn before deploying it. For this you have to install gunicorn with `sudo apt-get install gunicorn` and use pipenv to launch gunicorn.

```sh
workon YOUR-VIRTUALENV
env FLASK_ENV='production' gunicorn wsgi:application --bind 0.0.0.0:8080
```


## Other

Code formatting with [black](https://github.com/ambv/black).

```sh
# format all python modules
pipenv run black .
```