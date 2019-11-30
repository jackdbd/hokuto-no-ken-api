import os
from flask import Flask, json
import logging

# from werkzeug.contrib.fixers import ProxyFix
from dotenv import find_dotenv, load_dotenv
from .blueprints import api, flaskRestPlusApi, page
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


def export_api_as_postman_collection(app):
    """Generate a Postman collection from the Flask-RESTPlus Api instance."""
    # The Flask-RESTPlus Api's as_postman method requires SERVER_NAME to be set.
    # app.config["SERVER_NAME"] = "[HOST]:[PORT]"
    # Since the Postman collection generation is done on my machine (at least
    # for the time being), I pick localhost and the default port where the Flask
    # development server is running.
    app.config["SERVER_NAME"] = "127.0.0.1:5000"
    with app.app_context():
        urlvars = False  # Build query strings in URLs
        swagger = True  # Export Swagger specifications
        data = flaskRestPlusApi.as_postman(urlvars=urlvars, swagger=swagger)
        filename = f'postman_collection (generated on {data["timestamp"]}).json'
        with open(filename, "w") as f:
            f.write(json.dumps(data))
    
    # Flask blueprints with a subdomain set (as the FlaskRestPlus API blueprint
    # object in this Flask application) actually work if SERVER_NAME is NOT set.
    # https://github.com/pallets/flask/issues/998#issuecomment-45586187
    app.config["SERVER_NAME"] = None
