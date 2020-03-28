# Hokuto Flask

Hokuto no Ken [REST API](https://llpb3kmgw7.execute-api.eu-central-1.amazonaws.com/dev/api/v1/), powered by [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/).

Data from the [Hokuto Renkitōza](https://hokuto.fandom.com/wiki/Main_Page) wiki.

## Table of Contents

1. [Setup Python Virtual Environment](#setup-python-virtual-environment)
2. [Project Tasks](#project-tasks)
3. [Local Development](#local-development)
4. [Tests](#tests)
5. [AWS Configuration](#aws-configuration)

<div id='setup-python-virtual-environment'/>

## Setup Python Virtual Environment

This project uses [Python 3.7.2](https://www.python.org/downloads/release/python-372/). If you don't already have it, you can download Python 3.7.2 and install it with [pyenv](https://github.com/pyenv/pyenv).

```sh
pyenv install 3.7.2
```

Whenever you enter this project directory, pyenv selects the python version specified in the `.python-version` file (i.e. Python 3.7.2)

pyenv allows you to have multiple Python versions on your machine, but it does not prevent you from sharing the same environment across multiple projects. Since it's good practice to have an isolated environment for each project, you can use [pipenv](https://pipenv.readthedocs.io/en/latest/) to create a Python virtual environment for this project.

```sh
pipenv install --python=`pyenv which python`
```

Activate the virtual environment with:

```sh
pipenv shell
```

and install all project dependecies:

```sh
pipenv install --dev
```

<div id='project-tasks'/>

## Project Tasks

Pipenv is also really convenient as a CLI tool, and you can use it to perform several tasks while developing, testing, deploying this app.

The list of tasks for this project can be found in the `[scripts]` section of the `Pipfile`.

The first task to run is create a local [SQLite](https://sqlite.org/index.html) database and run all migrations.

This project uses [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) and [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/#) for database management and schema migrations.

Run all migrations with:

```sh
pipenv run db-upgrade-local
```

<div id='local-development'/>

## Local Development

This project uses a [Flask development server](https://flask.palletsprojects.com/en/1.1.x/server/) when running on your machine. Launch the development server with:

```sh
pipenv run dev
```

In alternative you could replace the Flask development server with gunicorn (+ speed, - debug info):

```sh
pipenv run dev-gunicorn
```

<div id='tests'/>

## Tests

This project uses [pytest](https://docs.pytest.org/en/latest/) for unit tests. A few of these tests generate mock data with [Mimesis](https://lk-geimfari.github.io/mimesis/) and perform some operations on an [in-memory SQLite database](https://sqlite.org/inmemorydb.html).

Run all tests with:

```sh
pipenv run test
```

<div id='aws-configuration'/>

## AWS Configuration

This project is deployed on AWS through [Zappa](https://www.zappa.io/). Apart from installing zappa as dev dependency, you will need to configure an [AWS named profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) and call it `zappa` (if you prefer to pick a different name, don't forget to update `profile_name` in `zappa_settings.json`).

Follow the guide [Creating IAM Users (Console)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console) to setup a new AWS IAM user with **programmatic access**.
