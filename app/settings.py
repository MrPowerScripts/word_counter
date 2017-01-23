# -*- coding: utf8 -*-
import os
import getpass
import logging as dlog
basedir = os.path.abspath(os.path.dirname(__file__))
logdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Logging configration
logfile = os.path.join(logdir, 'debug.log')
dlog.basicConfig(filename=logfile, level=dlog.INFO,
                 format="""[%(levelname)s] %(asctime)s.%(msecs)dGMT
                 %(module)s - %(funcName)s - %(lineno)d: %(message)s""",
                 datefmt="%Y-%m-%d %H:%M:%S")


class Config(object):
    LIVESERVER_PORT = 8000

    BASE_DIR = basedir

    TEMPLATES_AUTO_RELOAD = True

    # Database stuff

    if os.environ.get('word_match_SECRET_KEY'):
        SECRET_KEY = os.environ.get('word_match_SECRET_KEY')
    else:
        SECRET_KEY = "this_should_be_a_secret"

    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = ('postgresql:///wordapp')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
    SQLALCHEMY_RECORD_QUERIES = True

    if os.environ.get('word_match_DB_USER'):
        WORD_MATCH_DB_USER = os.environ.get('word_match_DB_USER')
    else:
        WORD_MATCH_DB_USER = getpass.getuser()

    if os.environ.get('word_match_DB_USER_PASSWORD'):
        WORD_MATCH_DB_USER_PASSWORD = os.environ.get('word_match_DB_USER_PASSWORD')
    else:
        WORD_MATCH_DB_USER_PASSWORD = "postgres"

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Assets
    ASSETS_DEBUG = True
    ASSETS_URL_EXPIRE = True

class ProdConfig(Config):
    ENV = "prod"
    TESTING = False
    DEBUG = False
    DEBUG_TB_ENABLED = False

    # Assets
    ASSETS_DEBUG = False
    ASSETS_URL_EXPIRE = True


class StagingConfig(Config):
    ENV = "staging"
    TESTING = False
    DEBUG = False
    WTF_CSRF_ENABLED = True


class DevConfig(Config):
    ENV = "dev"
    TESTING = False
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestConfig(Config):
    ENV = "test"
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = ('postgresql:///wordtest')
