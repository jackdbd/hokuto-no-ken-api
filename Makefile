ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SCRAPING_DIR:=${ROOT_DIR}/hokuto_scraping
DATA_DIR:=${ROOT_DIR}/hokuto_data
API_DIR:=${ROOT_DIR}/hokuto_flask

# Read the environment variables defined in the .env file
API_DOTENV:=${API_DIR}/.env
SECRET_KEY_PROD:=$(shell ack SECRET_KEY_PROD=.*$$ ${API_DIR}/.env | cut -d '=' -f2)
DB_URI_PROD:=$(shell ack DB_URI_PROD=postgres://.*\.com:[0-9]{4}/.*$$ ${API_DIR}/.env | cut -d '=' -f2)

# https://stackoverflow.com/a/8889085/3036129
.PHONY: help
help:
	@echo 'help       - Show this help.'
	@echo 'install    - Install the scrapers, the script to fetch the data'
	@echo '             from Redis and populate the database, and the Flask'
	@echo '             web application and Flask-RESTPlus API.'
	@echo 'hokuto.db  - Upgrade local development database (SQLite) to latest '
	@echo '             revision and populate it with data from Redis.'
	@echo 'deploy_api - Deploy the Flask web application and Flask-RESTPlus'
	@echo '             API on Heroku and sets all the environment variables '
	@echo '             required in production.'
	@echo 'test       - Run all tests.'
	@echo 'black      - Format all code with black.'
	@echo ''
	@echo 'Root directory: ${ROOT_DIR}'

# https://stackoverflow.com/a/3574387/3036129
.PHONY: install
install:
	cd ${SCRAPING_DIR} && pipenv install --dev
	cd ${DATA_DIR} && pipenv install --dev
	cd ${API_DIR} && pipenv install --dev

.PHONY: test
test:
	cd ${SCRAPING_DIR} && pipenv run pytest -v
	cd ${API_DIR} && pipenv run env FLASK_ENV='test' pytest -v

# Automated heroku deploy from subfolder \
https://stackoverflow.com/q/39197334/3036129
.PHONY: deploy_api
deploy_api:
	heroku config:set FLASK_ENV=production
	heroku config:set SECRET_KEY_PROD=${SECRET_KEY_PROD}
	heroku config:set DB_URI_PROD=${DB_URI_PROD}
	git subtree push --prefix hokuto_flask heroku master

hokuto.db:
	cd ${API_DIR} && pipenv run env FLASK_ENV='development' flask db upgrade
	cd ${DATA_DIR} && pipenv run python process_items.py -e development

.PHONY: black
black:
	cd ${SCRAPING_DIR} && pipenv run black .
	cd ${DATA_DIR} && pipenv run black .
	cd ${API_DIR} && pipenv run black .
