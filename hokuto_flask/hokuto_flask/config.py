import os
from dotenv import find_dotenv, load_dotenv


HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
load_dotenv(find_dotenv(".env"))


class ConfigDev(object):
    ENV = os.environ.get("ENV")
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY_DEV")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{ROOT}/{os.environ.get('DB_NAME_DEV')}"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ConfigTest(object):
    ENV = os.environ.get("ENV")
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.environ.get("SECRET_KEY_TEST")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///:memory:"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigProd(object):
    ENV = os.environ.get("ENV")
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY_PROD")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI_PROD")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
