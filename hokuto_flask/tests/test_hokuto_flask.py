import pytest
from hokuto_flask import app
# from .wsgi
from hokuto_flask.app import create_app


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4

@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()

    with flaskr.app.app_context():
        flaskr.init_db()

    yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])