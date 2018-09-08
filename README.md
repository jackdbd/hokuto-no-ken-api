# Hokuto no Ken API

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/jackdbd/hokuto-no-ken-api.svg?branch=master)](https://travis-ci.org/jackdbd/hokuto-no-ken-api) [![Python 3](https://pyup.io/repos/github/jackdbd/hokuto-no-ken-api/python-3-shield.svg)](https://pyup.io/repos/github/jackdbd/hokuto-no-ken-api/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

:warning: :construction_worker: WORK IN PROGRESS :building_construction: :construction:


## TODO: write brief description and instructions

Create the database updated to the latest revision. Run this command from the repository root directory (not from the `app` directory)

```shell
flask db upgrade
```

Populate the database by scraping the data from [Hokuto Renkitōza](http://hokuto.wikia.com/wiki/Main_Page). The spider will scrape all the Hokuto no Ken characters that have a wiki page, then an [Item Pipeline](https://doc.scrapy.org/en/latest/topics/item-pipeline.html) will populate all the tables.
