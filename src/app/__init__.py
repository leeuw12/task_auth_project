import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask


def configure_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('info.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def register_blueprints(app):
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config.from_object("config.ProductionConfig")
register_blueprints(app)
configure_logging()

