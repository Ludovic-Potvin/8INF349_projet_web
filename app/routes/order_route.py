from flask import Blueprint, request

from app.controllers.order_controller import OrderController

order = Blueprint('order', __name__, url_prefix='/order')

@order.route('/', methods=['POST'])
def post_order():
    data = request.get_json()

    return_object, error_code = OrderController.process_order(data)
    return return_object, error_code

@order.route('/<int:order_id>', methods=['GET'])
def get_order(order_id: int):
    error_code = 200
    return_object = {"message": "Commande traitée avec succès"}
    
    return_object, error_code = OrderController.get_order(order_id)
    return return_object, error_code