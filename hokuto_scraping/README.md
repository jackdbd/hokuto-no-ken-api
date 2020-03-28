# Hokuto Scraping

Scrape the [Hokuto Renkitōza](https://hokuto.fandom.com/wiki/Main_Page) wiki and collect all data in a Redis datastore.

## Installation

If you want just the spiders:

```sh
pipenv install
```

Otherwise, if you want to be able to test the code with [betamax](https://github.com/betamaxpy/betamax) and use the code formatter:

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

The `characters` spider is a [Scrapy Crawler](https://docs.scrapy.org/en/latest/topics/api.html#scrapy.crawler.Crawler). It scrapes all the data from the Hokuto no Ken characters (and the voice actors who dubbed them) that have a wiki page.

A scrapy [Item Pipeline](https://doc.scrapy.org/en/latest/topics/item-pipeline.html) sends this data to Redis (there must be a Redis server running on `localhost:6379`).

```sh
pipenv run scrape
```

When the script has finished (it should take ~3 minutes), check that the data is stored in Redis. You can use `redis-cli` and run the [LLEN](https://redis.io/commands/llen) command:

```sh
llen characters:items
```

or use a GUI like [Redis Desktop Manager](https://github.com/uglide/RedisDesktopManager).

If you want to rerun the script, remove the `characters` key from the Redis datastore with the [DEL command](https://redis.io/commands/del) first:

```sh
del characters
```

## Tests

This project uses [pytest](https://docs.pytest.org/en/latest/) for unit tests and [betamax](https://github.com/betamaxpy/betamax) for HTTP mock requests.

Run all tests with:

```sh
pipenv run test
```

## Other

Code formatting with [black](https://github.com/ambv/black).

```sh
pipenv run lint
```
