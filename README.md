# Hokuto no Ken API

TODO

:warning: :construction_worker: WORK IN PROGRESS :building_construction: :construction:


## Getting started

Create the database updated to the latest revision. Run this command from the repository root directory (not from the `app` directory)

```shell
flask db upgrade
```

Populate the database by scraping the data from [Hokuto Renkitōza](http://hokuto.wikia.com/wiki/Main_Page). The spider will scrape all the Hokuto no Ken characters that have a wiki page, then an [Item Pipeline](https://doc.scrapy.org/en/latest/topics/item-pipeline.html) will populate all the tables.

```shell
cd hokuto
python main.py -s characters
```

Start the Flask server and explore the API!

```shell
flask run
```


## Other

List all commands added by [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/).

```shell
flask db
```

Code formatting with [Black](https://github.com/ambv/black).

```shell
black .
```
