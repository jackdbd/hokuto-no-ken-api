import pytest
from hokuto_flask.app import create_app


@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()
    yield client


def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'No entries here so far' in rv.data
