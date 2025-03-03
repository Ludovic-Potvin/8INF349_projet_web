from app import create_app
from app.database import init_db
from app.database import *
import json
from flask import jsonify
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
    return jsonify({'Message': 'hello world'}), 200

@app.route('/products')
def products():
    list_of_products = get_products()
    print(json.dumps(list_of_products, indent=4) )
    print(type( list_of_products))
    return jsonify(list_of_products), 200

@app.route('/products/<int:product_id>')
def product(product_id):
    product = get_product(product_id)
    print(product)
    print(type(product))
    if product is None:
        return jsonify({'error': f'Product with id {product_id} not found'}), 404
    return jsonify(product), 200


if __name__ == '__main__':
    setup_logging()
    app.run(use_reloader=False)
