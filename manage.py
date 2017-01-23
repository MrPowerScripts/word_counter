#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import glob
from flask_script import Manager, Shell, Server, Command, Option
from flask_migrate import MigrateCommand

from app.word import create_app
from app.settings import DevConfig, ProdConfig, StagingConfig
from app.database import db
from app.models import *
from coverage import coverage
cov = coverage(branch=True, omit=['venv/*', '/tests.py'])

os.environ["word_match_MAN_EPOCH"] = str(int(time.time()))

if os.environ.get("word_match_ENV") == 'prod':
    app = create_app(ProdConfig)
elif os.environ.get("word_match_ENV") == 'staging':
    app = create_app(StagingConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')


# enable Gunicorn instead of the default Werkzeug server
class GunicornServer(Command):
    """Run the app within Gunicorn"""

    def get_options(self):
        from gunicorn.config import make_settings

        settings = make_settings()
        options = (
            Option(*klass.cli, action=klass.action)
            for setting, klass in settings.iteritems() if klass.cli
        )
        return options

    def run(self, *args, **kwargs):
        run_args = sys.argv[2:]
        run_args.append('manage:app')
        os.execvp('gunicorn', [''] + run_args)


manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db}


@manager.command
def liveserver(port=8001):
    from livereload import Server
    server = Server(app.wsgi_app)
    server.watch('app/static/public/css')
    server.watch('app/static/public/js/**')
    server.serve(port=port, host="0.0.0.0")


@manager.command
def gulp(task):
    """Run Gulp tasks"""
    os.system("gulp %s" % task)


@manager.command
def createdb(dbname):
    """provide a database name as a parameter to create the postgress db"""
    os.system("createdb -w %s" % dbname)


@manager.command
def removedb(dbname):
    """provide a database name as a parameter to delete the postgress db"""
    os.system("dropdb %s" % dbname)


@manager.command
def test():
    """Run the tests."""
    import pytest

    # Check to see if the test database exists before running tests.
    # If not, then create it.
    if not os.system('psql -lqt | cut -d \| -f 1 | grep -w wordtest | wc -l'):
        createdb('wordtest')

    exit_code = pytest.main([TEST_PATH, '--verbose'])

    return exit_code


@manager.command
def coverage():
    """Run the tests."""
    import pytest

    # Check to see if the test database exists before running tests.
    # If not, then create it.
    if not os.system("""psql -lqt | cut -d \|
     -f 1 | grep -w wordtest | wc -l"""):
        createdb('wordtest')

    cov.start()

    exit_code = pytest.main([TEST_PATH])

    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()

    return exit_code

manager.add_command("server", GunicornServer())
manager.add_command("werk", Server(host="0.0.0.0", port=8001))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
