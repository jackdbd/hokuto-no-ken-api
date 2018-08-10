import os


HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
# LOCAL_DB = os.environ.get("LOCAL_DB")


class ConfigDev(object):
    ENV = "development"
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY_DEV")
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///{ROOT}/{LOCAL_DB}"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
    # Show SQLAlchemy queries
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ConfigTest(object):
    ENV = "testing"
    DEBUG = True
    TESTING = True
    SECRET_KEY = "my-secret-key"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///:memory:"


class ConfigProd(object):
    ENV = "production"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY_PROD")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI_PROD")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
