from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from .routes.wiki_routes import wiki_routes
from .routes.auth_routes import auth_routes
from .logger.log import logger_initiation
from .controllers.mongo_service_model import  DBConnection
from .config import DevelopmentConfig

app = Flask(__name__, instance_relative_config=True)
CORS(app)
bcrypt = Bcrypt(app)
app_settings = DevelopmentConfig
app.config.from_object(app_settings)
app.register_blueprint(wiki_routes)
app.register_blueprint(auth_routes)

logger_initiation()
DBConnection.establish_connection()