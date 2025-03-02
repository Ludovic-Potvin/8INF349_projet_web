import json

import logging.config
import os

from flask import Flask

from app.database import init_db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
init_db()

logger = logging.getLogger(app.config['LOGGER_NAME'])


def setup_logging():
    """Set up the logger configuration."""
    config_file = app.config['LOGGER_CONFIG_FILE']

    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])

    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)

@app.route('/')
def hello_world():  # todo put application's code here
    app.logger.info('Hello World')
    return 'Hello World!'

if __name__ == '__main__':
    setup_logging()
    app.run(use_reloader=False)
