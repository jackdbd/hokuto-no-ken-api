import os
from dotenv import load_dotenv


HERE = os.path.abspath(os.path.dirname(__file__))
DOTENV_PATH = os.path.abspath(os.path.join(HERE, "..", ".env"))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
load_dotenv(DOTENV_PATH)

FLASK_ENV = os.environ.get("FLASK_ENV")

if FLASK_ENV == "development":
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY_DEV")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{ROOT}/{os.environ.get('DB_NAME_DEV')}"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
elif FLASK_ENV == "staging":
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY_STAG")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI_STAG")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
elif FLASK_ENV == "production":
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY_PROD")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI_PROD")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
else:
    msg = f"""FLASK_ENV is {FLASK_ENV}.
    These settings are for these environments:
    development, staging, production.
    Set FLASK_ENV in {DOTENV_PATH}."""
    raise KeyError(msg)
