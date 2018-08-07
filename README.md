# Hokuto no Ken API

An API built by scraping the [Hokuto Renkitōza](http://hokuto.wikia.com/wiki/Main_Page) wiki.

Powered by [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/).

:warning: :construction_worker: WORK IN PROGRESS :building_construction: :construction:


## Getting started

First of all, you need to create a conda environment. You can clone the environment I used:

```shell
conda env create -f environment.yml
```

Then activate it:

```shell
source activate hokuto-no-ken-api
```

*Note: I previously tried to create a python 3.6 virtual environment with virtualenvwrapper but failed when trying to install Scrapy. I think this is because of some issues with Twisted.*

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

Lint with [Black](https://github.com/ambv/black).

```shell
black .
```
