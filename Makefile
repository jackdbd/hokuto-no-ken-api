ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SCRAPING_DIR:=${ROOT_DIR}/hokuto_scraping
DATA_DIR:=${ROOT_DIR}/hokuto_data
API_DIR:=${ROOT_DIR}/hokuto_flask
API_DOTENV:=${API_DIR}/.env
VARIABLE=`cat $(API_DOTENV)`

# https://stackoverflow.com/a/8889085/3036129
.PHONY: help
help:
	@echo 'help       - Show this help.'
	@echo 'install    - Install the scrapers, the script to fetch the data'
	@echo '             from Redis and populate the database, and the Flask'
	@echo '             web application and Flask-RESTPlus API.'
	@echo 'deploy_api - Deploy the Flask web application and Flask-RESTPlus'
	@echo '             API on Heroku.'
	@echo 'test       - Run all tests.'
	@echo ${API_DIR}
	@echo ${API_DOTENV}
	@echo ${VARIABLE}

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
	# TODO: how to get SECRET_KEY_PROD, DB_URI from .env file and set them here?
	git subtree push --prefix hokuto_flask heroku master
