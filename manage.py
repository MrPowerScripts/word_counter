#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import glob
from flask_script import Manager, Shell, Server, Command, Option
from flask_migrate import MigrateCommand

from app.word import create_app
from app.settings import DevConfig, ProdConfig
from app.extensions import db
from app.models import *

os.environ["WM_MAN_EPOCH"] = str(int(time.time()))

if os.environ.get("WM_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

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

manager.add_command("werk", Server(host="0.0.0.0", port=8001))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
