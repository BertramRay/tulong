import os


class BaseConfig:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "temp")


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    DOMAIN = "http://tulong.com"
    JWT_SECRET = "tulong666"
    RESULT_URL = DOMAIN + "/temp"


class ProductionConfig(BaseConfig):
    ENV = "production"
    DOMAIN = "https://tulong.bertyblog.link"
    JWT_SECRET = "tulong666"
    RESULT_URL = DOMAIN + "/temp"


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
