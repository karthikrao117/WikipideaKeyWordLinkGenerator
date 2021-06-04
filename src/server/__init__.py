import os

from flask import Flask
from .routes.wikigenerator_route import wikigenerator
from .logger.log import logger_initiation
from .controllers.mongo_db_access import  DBConnection

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(wikigenerator)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    logger_initiation()
    DBConnection.establish_connection()
    DBConnection.db_instance_provider()
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
