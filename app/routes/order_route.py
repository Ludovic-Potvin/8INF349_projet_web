from flask import Blueprint, request, render_template, jsonify
import app
from app.controllers.order_controller import OrderController
from app.controllers.product_controller import ProductController

order = Blueprint('order', __name__, url_prefix='/order')

@order.route('/', methods=['POST'])
def post_order():
    app.logger.info("Found route post_order")
    data = request.get_json()

    return_object, error_code = OrderController.process_order(data)
    return return_object, error_code

@order.route('/<int:id>', methods=['PUT'])
def order_update(id):
    data = request.get_json()
    return OrderController.update(id, data)


@order.route('/<int:order_id>', methods=['GET'])
def get_order(order_id: int):
    app.logger.info("Found route get_order")
    return_object = {"message": "Commande traitée avec succès"}
    
    return_object, error_code = OrderController.get_order(order_id)
    print(return_object.product_id)
    return return_object.to_dict(), error_code


@order.route('/panier/<int:order_id>', methods=['GET'])
def get_panier(order_id: int):
    app.logger.info("Found route get_order")
    return_object = {"message": "Commande traitée avec succès"}
    
    return_object, error_code = OrderController.get_order(order_id)
    products = ProductController.get_product_by_id(return_object.product_id) #TO-DO CHANGE THIS TO RETURN MULTIPLE PRODUCTS
    print(products)
    return render_template('panier.html', order=return_object, products=products), error_code

@order.route('/shipping_form/<int:id>', methods=['GET'])
def shipping_form(id: int):
    return render_template('shipping_form.html', id=id)

@order.route('/paiement/<int:id>', methods=['GET'])
def paiement_form(id: int):
    return_object, error_code = OrderController.get_order(id)
    return render_template('paiement.html', id=id, order=return_object), error_code

@order.route('/confirmation/<int:id>', methods=['GET'])
def confirmation(id: int):
    return_object, error_code = OrderController.get_order(id)
    products = ProductController.get_product_by_id(return_object.product_id) #TO-DO CHANGE THIS TO RETURN MULTIPLE PRODUCTS
    return render_template('confirmation.html', id=id, order=return_object, products=products), error_code