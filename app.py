from flask import request, jsonify, make_response

from app import create_app
from app.database import init_db
from app.controllers.post_order import *

app = create_app()

init_db()

@app.route('/')
def hello_world():  # todo put application's code here
    return 'Hello World!'

@app.route('/order', methods=['POST'])
def post_order():
    data = request.get_json()
    error_code = 200
    return_object = {"message": "Commande traitée avec succès"}

    product = data.get('product', {})
    id = product.get('id', {})
    quantity = product.get('quantity', {})

    return_object, error_code = process_order(product, id, quantity)
    return return_object, error_code

if __name__ == '__main__':
    app.run()
