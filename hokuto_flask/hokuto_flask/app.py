import os
from flask import Flask
import logging

# from werkzeug.contrib.fixers import ProxyFix
from dotenv import find_dotenv, load_dotenv
from .blueprints import api, page
from .extensions import db, migrate


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

HERE = os.path.abspath(os.path.dirname(__file__))
DEFAULT_SETTINGS_PATH = os.path.abspath(os.path.join(HERE, "settings.py"))


def create_app(config_filename=DEFAULT_SETTINGS_PATH):
    """Create a Flask WSGI application using the app factory pattern."""

    app = Flask(__name__.split(".")[0])
    logger.info(f"Flask App instance id: {id(app)}")
    app.config.from_pyfile(config_filename)
    if app.config["FLASK_ENV"] == "development":
        for k in app.config:
            logger.debug(f'{k}: {app.config[k]}')
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    app.register_blueprint(api)
    app.register_blueprint(page)
    extensions(app)
    return app


def extensions(app):
    """Register 0 or more extensions (mutates the app passed in)."""
    db.init_app(app)
    migrate.init_app(app, db)
    return None
