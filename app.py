from flask import request
from flask import jsonify

from app import create_app
from app.database import init_db, check_product

app = create_app()

init_db()

@app.route('/')
def hello_world():  # todo put application's code here
    return 'Hello World!'

@app.route('/order', methods=['POST'])
def post_order():
    data = request.get_json()
    if not 'product' in data or 'id' not in data['product'] or 'quantity' not in data['product'] or data['product']['quantity'] < 1 :
        return jsonify({
                        "errors" : {
                            "product": {
                                "code": "Missing-fields",
                                "name": "La création d'une commande nécessite un produit"
                            }
                        }
                    }), 422
    return check_product(data['product']['id'], data['product']['quantity'])

if __name__ == '__main__':
    app.run()
