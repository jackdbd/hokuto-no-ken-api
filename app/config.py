import os


HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
LOCAL_DB = os.environ.get("LOCAL_DB")


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{ROOT}/{LOCAL_DB}"
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    # Show SQLAlchemy queries
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
