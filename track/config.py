import os
import random

class Config():
    DEBUG = False
    TESTING = False
    MONGO_URI = 'mongodb://localhost:27017/track'
    CACHE_TYPE = 'null'


class ProductionConfig(Config):
    MONGO_URI = os.environ.get('TRACKER_MONGO_URI', None)
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = os.environ.get('TRACKER_REDIS_HOST')
    CACHE_REDIS_PORT = os.environ.get('TRACKER_REDIS_PORT')


class DevelopmentConfig(Config):
    DEBUG = True
    CACHE_TYPE = 'simple'


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/track_{rand}'.format(rand=random.randint(0, 1000))
