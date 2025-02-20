from app import create_app
from app.database import init_db
from app.database import *
import json

app = create_app()

init_db()

@app.route('/')
def hello_world():  # todo put application's code here
    return 'Hello, World!'

@app.route('/products')
def products():
    list_of_products = get_products()
    print(json.dumps(list_of_products, indent=4) )
    print(type( list_of_products))
    return jsonify(list_of_products), 200

@app.route('/product/<int:product_id>')
def product(product_id):
    product = get_product(product_id)
    print(product)
    print(type(product))
    if product is None:
        return jsonify({'error': f'Product with id {product_id} not found'}), 404
    return jsonify(product), 200

if __name__ == '__main__':
    app.run()
