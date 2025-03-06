import json
import os
from logging.config import dictConfig

from flask import Flask

from config import Config
from app.routes import product_route, order_route

def setup_logging(log_file, log_directory):
    """Set up the logger configuration."""
    config_file = log_file

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    with open(config_file) as f_in:
        log_config = json.load(f_in)
    dictConfig(log_config)


def create_app():
    # Load app config
    setup_logging(Config.LOGGER_CONFIG_FILE, Config.LOG_DIR)

    app = Flask(__name__)
    app.config.from_object(Config)

    app.logger.debug("Test log from the app logger")

    app.register_blueprint(product_route.products)
    app.register_blueprint(order_route.order)

    return app