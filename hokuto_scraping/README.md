# Hokuto Scraping

Scrape the [Hokuto Renkitōza](https://hokuto.fandom.com/wiki/Main_Page) wiki and collect all data in a Redis datastore.

## Installation

If you want just the spiders:

```sh
pipenv install
```

Otherwise, if you want to be able to test the code with [Betamax](https://github.com/betamaxpy/betamax) and use the code formatter:

```sh
pipenv install --dev
```

If your editor of choice is VS code, set the python path in `.vscode/settings.json`:

```json
{
    "python.pythonPath": "<COPY THE OUTPUT OF pipenv --venv HERE>/bin/python"
}
```

You will also need a Redis datastore to connect to. I start a [redis-server](https://redis.io/topics/quickstart) on my machine.

## Usage

The `characters` spider scrapes all the data from the Hokuto no Ken characters that have a wiki page.

A scrapy [Item Pipeline](https://doc.scrapy.org/en/latest/topics/item-pipeline.html) sends this data to Redis (there must be a Redis server running on `localhost:6379`).

```sh
pipenv run scrape

# OR
pipenv --venv  # to know the name of YOUR-VIRTUALENV
workon YOUR-VIRTUALENV
python manage.py -s characters
```

When the script has finished (it should take ~5 minutes), check that the data is stored in Redis. You can use `redis-cli` and run this simple command:

```sh
llen characters:items
```

## Tests

This project uses [pytest](https://docs.pytest.org/en/latest/) for unit tests.

Run all tests with:

```sh
pipenv run test
```

## Other

Code formatting with [black](https://github.com/ambv/black).

```sh
# format all python modules
pipenv run lint
```
