from flask import Flask
from app.config import Config
from app.blueprints import api, page
from app.extensions import db, migrate


def create_app():
    """Create a Flask WSGI application using the app factory pattern."""
    app = Flask(__name__)
    app.config.from_object(Config)
    # print("app.config\n", app.config)
    app.register_blueprint(api)
    app.register_blueprint(page)
    extensions(app)
    return app


def extensions(app):
    """Register 0 or more extensions (mutates the app passed in)."""
    db.init_app(app)
    migrate.init_app(app, db)
    return None
