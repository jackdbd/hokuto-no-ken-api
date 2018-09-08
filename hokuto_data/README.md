# Hokuto Data

Populate database tables with the data found in Redis.


## Installation

```sh
pipenv install
```


## Usage

```sh
pipenv run python process_items.py

# OR
pipenv --venv  # to know the name of YOUR-VIRTUALENV
workon YOUR-VIRTUALENV
python process_items.py
```


## Seed DB with some fakes

```sh
pipenv run python seed_db.py
```


## Other

Code formatting with [black](https://github.com/ambv/black).

```sh
pipenv run black .
```
