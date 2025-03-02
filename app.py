
import json

import logging.config
import os

from flask import Flask
from flask import jsonify

from app.database import init_db
from config import Config


from app import create_app
from app.database import init_db, update_order_shipping, update_order_card

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


@app.route('/order/<int:id>', methods=['PUT'])
def order_update(id):
    data = request.get_json()
    #Only one type of data check
    if 'order' in data and 'credit_card' in data:
        return jsonify({"errors": {
                    "order": {
                        "code": "Bad Request",
                        "name": "Un seul type d'information peut être modifier à la fois"
                        }
                    }
                }), 400

    if 'order' in data:
        return update_order_shipping(id, data)
    elif 'credit_card' in data:
        return update_order_card(id, data)
    else:
        return jsonify({"error": "tea - how did you end up here"}), 418


if __name__ == '__main__':
    setup_logging()
    app.run(use_reloader=False)
