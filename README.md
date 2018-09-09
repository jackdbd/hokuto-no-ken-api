# Hokuto no Ken API

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/jackdbd/hokuto-no-ken-api.svg?branch=master)](https://travis-ci.org/jackdbd/hokuto-no-ken-api) [![Code Coverage](https://codecov.io/gh/jackdbd/hokuto-no-ken-api/coverage.svg)](https://codecov.io/gh/jackdbd/hokuto-no-ken-api) [![Python 3](https://pyup.io/repos/github/jackdbd/hokuto-no-ken-api/python-3-shield.svg)](https://pyup.io/repos/github/jackdbd/hokuto-no-ken-api/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) 

:warning: :construction_worker: WORK IN PROGRESS :building_construction: :construction:


## Installation

You can use the `Makefile` included in this repository to install all the components.

```sh
make install
```

This command will:

1. create the environment for the [scrapy spiders](https://github.com/jackdbd/hokuto-no-ken-api/tree/master/hokuto_scraping);
2. create the environment for the [script](https://github.com/jackdbd/hokuto-no-ken-api/tree/master/hokuto_data) that populates the database with data found in Redis;
3. create the environment for the [Flask web application and Flask-RestPlus API](https://github.com/jackdbd/hokuto-no-ken-api/tree/master/hokuto_flask).


## Deploy the API on Heroku

```sh
make deploy_api
```
