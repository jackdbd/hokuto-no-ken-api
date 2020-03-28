# Hokuto Data

Populate database tables with the data found in Redis.

## Installation

```sh
pipenv install --dev
```

If your editor of choice is VS code, set the python path in `.vscode/settings.json`:

```json
{
    "python.pythonPath": "<COPY THE OUTPUT OF pipenv --venv HERE>/bin/python"
}
```

## Usage

You can populate the SQLite database with some fakes, with [Mimesis](https://github.com/lk-geimfari/mimesis).

```sh
pipenv run fakes
```

Otherwise, once you have stored the scraped data in Redis (see [Hokuto Scraping README](https://github.com/jackdbd/hokuto-no-ken-api/tree/master/hokuto_scraping)), dump everything in the database with this command:

```sh
pipenv run dump
```

## Other

Code formatting with [black](https://github.com/ambv/black).

```sh
pipenv run lint
```
