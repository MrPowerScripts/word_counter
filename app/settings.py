# -*- coding: utf8 -*-
import os
import getpass
import logging as dlog
basedir = os.path.abspath(os.path.dirname(__file__))
logdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Logging configration
logfile = os.path.join(logdir, 'debug.log')
dlog.basicConfig(filename=logfile, level=dlog.DEBUG,
                 format="""[%(levelname)s] %(asctime)s.%(msecs)dGMT
                 %(module)s - %(funcName)s - %(lineno)d: %(message)s""",
                 datefmt="%Y-%m-%d %H:%M:%S")

class Config(object):
    LIVESERVER_PORT = 8000
    BASE_DIR = basedir
    TEMPLATES_AUTO_RELOAD = True

    # Database stuff
    SQLALCHEMY_DATABASE_URI = ('postgresql:///wordapp')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
    DB_USER = getpass.getuser()
    DB_USER_PASSWORD = "postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Assets
    ASSETS_DEBUG = True
    ASSETS_URL_EXPIRE = True

class ProdConfig(Config):
    ENV = "prod"
    TESTING = False
    DEBUG = False

    # Assets
    ASSETS_DEBUG = False
    ASSETS_URL_EXPIRE = True

class DevConfig(Config):
    ENV = "dev"
    TESTING = False
    DEBUG = True
