# Hokuto Flask

Hokuto no Ken [REST API](https://floating-headland-89373.herokuapp.com/api/v1/).

Data from the [Hokuto Renkitōza](http://hokuto.wikia.com/wiki/Main_Page) wiki.

Powered by [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/).


## Installation

```sh
pipenv install
```


## Usage

```
pipenv run flask run
```


## Migrations

```sh
pipenv run flask db init --multidb
pipenv run flask db migrate
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

