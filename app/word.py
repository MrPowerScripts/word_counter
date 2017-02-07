from flask import Flask

from .extensions import (
    db,
    migrate
)
from . import (
    home,
    api
)

from app.settings import Config, ProdConfig, DevConfig

from assets import assets

def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_blueprints(app)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    assets.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    app.register_blueprint(api.controllers.mod_api, url_prefix='/api')
    app.register_blueprint(home.controllers.mod_home)
    return None
