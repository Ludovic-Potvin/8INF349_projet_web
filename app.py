from flask import request, jsonify, make_response

from app import create_app
from app.database import init_db
from app.controllers.order_controller import OrderController

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
    
    return_object, error_code = OrderController.process_order(data)
    return return_object, error_code

if __name__ == '__main__':
    app.run()
