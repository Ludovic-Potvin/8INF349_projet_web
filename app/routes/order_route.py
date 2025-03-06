from flask import Blueprint, request, current_app
from app.controllers.order_controller import OrderController

order = Blueprint('order', __name__, url_prefix='/order')

@order.route('/', methods=['POST'])
def post_order():
    current_app.logger.info("Found route post_order")
    data = request.get_json()

    return_object, error_code = OrderController.process_order(data)
    return return_object, error_code

@order.route('/<int:order_id>', methods=['GET'])
def get_order(order_id: int):
    current_app.logger.info("Found route get_order")
    return_object = {"message": "Commande traitée avec succès"}
    
    return_object, error_code = OrderController.get_order(order_id)
    return return_object.to_dict(), error_code

@order.route('/<int:id>', methods=['PUT'])
def order_update(id):
    data = request.get_json()
    return OrderController.update(id, data)