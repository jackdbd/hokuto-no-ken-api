import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from dotenv import find_dotenv, load_dotenv
from .config import ConfigDev, ConfigTest, ConfigProd
from .blueprints import api, page
from .extensions import db, migrate


load_dotenv(find_dotenv(".env"))
ENV = os.environ.get("ENV")


def create_app():
    """Create a Flask WSGI application using the app factory pattern."""
    app = Flask(__name__)
    if ENV == "dev":
        app.config.from_object(ConfigDev)
    elif ENV == "test":
        app.config.from_object(ConfigTest)
    elif ENV == "prod":
        app.config.from_object(ConfigProd)
    else:
        raise KeyError("Set ENV environment variable")

    assert ENV == app.config["ENV"]
    # for k in app.config:
    #     print(k, app.config[k])
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
