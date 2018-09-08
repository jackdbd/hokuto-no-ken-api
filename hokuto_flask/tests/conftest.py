import os
import pytest
from hokuto_flask.app import create_app
from hokuto_flask.extensions import db as _db
from hokuto_flask.blueprints.api.models import CharacterModel
from .factories import make_character


HERE = os.path.abspath(os.path.dirname(__file__))
TESTS_SETTINGS_PATH = os.path.abspath(os.path.join(HERE, "settings.py"))


@pytest.fixture
def app():
    """An application for the tests."""
    _app = create_app(config_filename=TESTS_SETTINGS_PATH)
    ctx = _app.test_request_context()
    ctx.push()
    yield _app
    ctx.pop()


@pytest.fixture
def db_empty(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def db_full(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    # populate the database with some characters
    for i in range(10):
        d = make_character(seed=i)
        character = CharacterModel(**d)
        character.save()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()
