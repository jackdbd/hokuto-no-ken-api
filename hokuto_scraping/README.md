# Hokuto Scraping

Scrape the [Hokuto Renkitōza](http://hokuto.wikia.com/wiki/Main_Page) wiki and collect all data in a Redis datastore.


## Installation

```
pipenv install
```


## Usage

The `characters` spider scrapes all the data from the Hokuto no Ken characters that have a wiki page.

A scrapy [Item Pipeline](https://doc.scrapy.org/en/latest/topics/item-pipeline.html) sends this data to Redis (there must be a Redis server running on `localhost:6379`).

```
pipenv run python manage.py -s characters
```

When the script has finished (it should take ~5 minutes), check that the data is stored in Redis. You can use `redis-cli` and run this simple command:

```
llen characters:items
```


## Other

Code formatting with [black](https://github.com/ambv/black).

```
# format all python modules
pipenv run black .
```
