from flask import Blueprint, render_template

from app.controllers.product_controller import ProductController
from app.controllers.order_controller import OrderController

page = Blueprint('page', __name__, url_prefix='/page')

@page.route('/products')
def get_products_page():
    products = ProductController.get_products()
    return render_template('products.html', products=products)

@page.route('/products/<int:product_id>')
def get_product_page(product_id: int):
    product = ProductController.get_product_by_id(product_id)
    return render_template('product.html', product=product)

@page.route('/panier/<int:order_id>', methods=['GET'])
def get_panier(order_id: int):
    return_object = {"message": "Commande traitée avec succès"}
    
    return_object, error_code = OrderController.get_order(order_id)
    products = ProductController.get_product_by_id(return_object.product_id) #TO-DO CHANGE THIS TO RETURN MULTIPLE PRODUCTS
    print(products)
    return render_template('panier.html', order=return_object, products=products), error_code

@page.route('/shipping_form/<int:id>', methods=['GET'])
def shipping_form(id: int):
    return render_template('shipping_form.html', id=id)

@page.route('/paiement/<int:id>', methods=['GET'])
def paiement_form(id: int):
    return_object, error_code = OrderController.get_order(id)
    return render_template('paiement.html', id=id, order=return_object), error_code

@page.route('/confirmation/<int:id>', methods=['GET'])
def confirmation(id: int):
    return_object, error_code = OrderController.get_order(id)
    products = ProductController.get_product_by_id(return_object.product_id) #TO-DO CHANGE THIS TO RETURN MULTIPLE PRODUCTS
    return render_template('confirmation.html', id=id, order=return_object, products=products), error_code