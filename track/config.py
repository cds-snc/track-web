import os
import sys
import random

from azure.keyvault import KeyVaultClient
from msrestazure.azure_active_directory import MSIAuthentication, ServicePrincipalCredentials

A_DAY = 60 * 60 * 24

class Config:
    DEBUG = False
    TESTING = False
    MONGO_URI = "mongodb://localhost:27017/track"
    CACHE_TYPE = "null"

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    if os.environ.get("TRACKER_KEYVAULT_URI", None) is None or os.environ.get("SECRET_NAME_RO", None) is None:
        # Error and crash hard: Production should be configured as expected.
        sys.exit("KeyVault uri or secret name missing from local environment.")
                  
    KV_URI = os.environ.get("TRACKER_KEYVAULT_URI")
    SECRET_NAME = os.environ.get("SECRET_NAME_RO")
    CREDS = MSIAuthentication(resource='https://vault.azure.net')
    KEYVAULT = KeyVaultClient(CREDS)
    MONGO_URI = KEYVAULT.get_secret(KV_URI, SECRET_NAME, "").value

    CACHE_TYPE = "filesystem"
    CACHE_DIR = os.environ.get("TRACKER_CACHE_DIR", "./.cache")
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("TRACKER_CACHE_TIMEOUT", A_DAY))

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
