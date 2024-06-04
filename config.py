import os


DB_USER = os.environ.get("DB_USER") or "task"
DB_PASSWORD = os.environ.get("DB_PASSWORD") or 1
DB_HOST = os.environ.get("DB_HOST") or  "localhost"
DB_PORT = os.environ.get("DB_PORT") or 5432
DB_NAME = os.environ.get("DB_NAME") or "task"


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY  = os.environ.get("SECRET_KEY") or "secret_key_for_flask_app"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI  =  (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    WTF_CSRF_ENABLED  = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI  =  (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}