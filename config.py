import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'ThiSiSSecret'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:password@localhost/school_year'
    APP_SETTINGS = "config.DevelopmentConfig"
    UPLOAD_FOLDER = 'uploads'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True