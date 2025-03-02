from flask import request, jsonify, make_response

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
    error_code = 200
    return_object = {"message": "Commande traitée avec succès"}

    product = data.get('product', {})
    id = product.get('id', {})
    quantity = product.get('quantity', {})

    if product and id and quantity and quantity >= 1 :
        product = check_product(id)
        if not product or quantity > product.in_stock:
            error_code = 422
            return_object = {
                                "errors" : {
                                    "product": {
                                        "code": "Out-of-inventory",
                                        "name": "Le produit demandé n'est pas en inventaire"
                                    }
                                }
                            }
    else:
        error_code = 422
        return_object = {
                            "errors" : {
                                "product": {
                                    "code": "Missing-fields",
                                    "name": "La création d'une commande nécessite un produit"
                                }
                            }
                        }
    return jsonify(return_object), error_code

if __name__ == '__main__':
    app.run()
