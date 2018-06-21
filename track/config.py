import logging
import os
import random

class Config():
    DEBUG = False
    TESTING = False
    MONGO_URI = 'mongodb://localhost:27017/track'
    CACHE_TYPE = 'null'
    LOGLEVEL = logging.INFO
    SYSLOG_ADDRESS = '/var/run/syslog'

A_DAY = 60*60*24
class ProductionConfig(Config):
    MONGO_URI = os.environ.get('TRACKER_MONGO_URI', None)
    CACHE_TYPE = 'filesystem'
    CACHE_DIR = os.environ.get('TRACKER_CACHE_DIR', '.')
    CACHE_DEFAULT_TIMEOUT = os.environ.get('TRACKER_CACHE_TIMEOUT', A_DAY)
    LOGLEVEL = logging.WARNING


class DevelopmentConfig(Config):
    DEBUG = True
    CACHE_TYPE = 'simple'
    LOGLEVEL = logging.DEBUG


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/track_{rand}'.format(rand=random.randint(0, 1000))
    LOGLEVEL = logging.CRITICAL
