from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from .config import Config
from .blueprints import api, page
from .extensions import db, migrate


def create_app():
    """Create a Flask WSGI application using the app factory pattern."""
    app = Flask(__name__)
    app.config.from_object(Config)
    # print("app.config\n", app.config)
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
