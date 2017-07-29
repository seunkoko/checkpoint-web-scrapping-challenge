import os
import dotenv

from os.path import join, dirname

dotenv.load()


class Config(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfiguration(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfiguration(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + Config.BASE_DIR \
                              + "/test_db.sqlite"


app_configuration = {
    'production': Config,
    'development': DevelopmentConfiguration,
    'testing': TestingConfiguration
}

