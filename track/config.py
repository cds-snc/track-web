import os
import random


class Config:
    DEBUG = False
    TESTING = False
    MONGO_URI = "mongodb://localhost:27017/track"
    CACHE_TYPE = "null"

    @staticmethod
    def init_app(app):
        pass


A_DAY = 60 * 60 * 24
class ProductionConfig(Config):
    MONGO_URI = os.environ.get("TRACKER_MONGO_URI", None)
    CACHE_TYPE = "filesystem"
    CACHE_DIR = os.environ.get("TRACKER_CACHE_DIR", ".")
    CACHE_DEFAULT_TIMEOUT = os.environ.get("TRACKER_CACHE_TIMEOUT", A_DAY)

    @staticmethod
    def init_app(app):
        Config.init_app(app)

        import logging
        from logging.handlers import SysLogHandler

        handler = SysLogHandler(address=os.environ.get("TRACKER_SYSLOG", "/dev/log"))
        handler.setLevel(logging.ERROR)
        app.logger.addHandler(handler)


class DevelopmentConfig(Config):
    DEBUG = True
    CACHE_TYPE = "simple"


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = "mongodb://localhost:27017/track_{rand}".format(
        rand=random.randint(0, 1000)
    )


config = {
    "testing": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
