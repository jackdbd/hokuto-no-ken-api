# Hokuto Flask

Hokuto no Ken [REST API](https://floating-headland-89373.herokuapp.com/api/v1/), powered by [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/).

Data from the [Hokuto Renkitōza](http://hokuto.wikia.com/wiki/Main_Page) wiki.


## Installation

```sh
pipenv install
```


## Usage

```sh
pipenv run flask run
```


## Migrations

```sh
# Init the migrations repository (only once)
pipenv run flask db init

# Create the migration script (every time there is a change in the schema)
pipenv run flask db migrate

# Run all migration scripts
pipenv run flask db upgrade
```


## Tests

```sh
pipenv run pytest
```


## Other

Code formatting with [black](https://github.com/ambv/black).

```sh
# format all python modules
pipenv run black .
```

## TODO: document how to run tests

```sh
pipenv run pytest
```

```sh
http://flask.pocoo.org/docs/1.0/testing/
```


## Run gunicorn

It might be useful to try running the application with gunicorn before deploying it. For this you have to install gunicorn with `sudo apt-get install gunicorn` and use pipenv to launch gunicorn.

```sh
pipenv run gunicorn wsgi:application --bind 0.0.0.0:8080
```
