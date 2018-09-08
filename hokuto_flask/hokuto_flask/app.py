import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from dotenv import find_dotenv, load_dotenv
from .blueprints import api, page
from .extensions import db, migrate


HERE = os.path.abspath(os.path.dirname(__file__))
DEFAULT_SETTINGS_PATH = os.path.abspath(os.path.join(HERE, "settings.py"))


def create_app(config_filename=DEFAULT_SETTINGS_PATH):
    """Create a Flask WSGI application using the app factory pattern."""
    app = Flask(__name__.split(".")[0])
    app.config.from_pyfile(config_filename)
    if app.config["FLASK_ENV"] in ("development", "staging"):
        print("Flask App Config...............")
        for k in app.config:
            print(k, app.config[k])
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.register_blueprint(api)
    app.register_blueprint(page)
    extensions(app)
    return app


def extensions(app):
    """Register 0 or more extensions (mutates the app passed in)."""
    db.init_app(app)
    migrate.init_app(app, db)
    return None
