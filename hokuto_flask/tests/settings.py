import os
from dotenv import load_dotenv


HERE = os.path.abspath(os.path.dirname(__file__))
DOTENV_PATH = os.path.abspath(os.path.join(HERE, "..", ".env"))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
load_dotenv(DOTENV_PATH)

FLASK_ENV = os.environ.get("FLASK_ENV")
if FLASK_ENV == "test":
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.environ.get("SECRET_KEY_TEST")
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
else:
    msg = f"""FLASK_ENV is {FLASK_ENV}.
    These settings are for this environment: test
    Set FLASK_ENV in {DOTENV_PATH}."""
    raise KeyError(msg)
