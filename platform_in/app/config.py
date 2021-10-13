import os
import logging

logging.basicConfig(level=logging.INFO)

basedir = os.path.abspath(os.path.dirname(__file__))


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        logging.error(message)
        raise Exception(message)


class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = True
    CSRF_ENABLED = True

    OBSERVATIONS_ENDPOINT = get_env_variable("OBSERVATIONS_ENDPOINT")
    DATASTREAMS_ENDPOINT = get_env_variable("DATASTREAMS_ENDPOINT")

    ELASTIC_APM = {
        "SERVICE_NAME": get_env_variable("ELASTIC_SERVICE_NAME"),
        "SECRET_TOKEN": get_env_variable("ELASTIC_SECRET_TOKEN"),
        "SERVER_URL": get_env_variable("ELASTIC_SERVER_URL"),
        "DEBUG": True,
    }

    ll = get_env_variable("LOG_LEVEL")
    try:

        LOG_LEVEL = {0: logging.ERROR, 1: logging.WARN, 2: logging.INFO}[int(ll)]
    except KeyError:
        LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    TESTING = False
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
