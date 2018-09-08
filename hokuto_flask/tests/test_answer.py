import pytest
from hokuto_flask import app
from hokuto_flask.app import create_app


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4
