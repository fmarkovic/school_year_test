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
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True