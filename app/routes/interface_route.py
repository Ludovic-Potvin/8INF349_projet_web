from flask import Blueprint, render_template, request, g

from app.controllers.product_controller import ProductController
from app.controllers.order_controller import OrderController
import uuid
from app.panier_helper import get_panier_redis, add_product_to_cart, set_panier_redis

page = Blueprint('page', __name__, url_prefix='/page')

@page.route('/products')
def get_products_page():
    products = ProductController.get_products()
    return render_template('products.html', products=products)

@page.route('/products/<int:product_id>')
def get_product_page(product_id: int):
    product = ProductController.get_product_by_id(product_id)
    return render_template('product.html', product=product)

@page.route('/panier', methods=['GET'])
def get_panier():
    products = get_panier_redis()
    print(products)
    return render_template('panier.html', products=products)

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
    products = [ProductController.get_product_by_id(product_id) for product_id in return_object.product_links]
    return render_template('confirmation.html', id=id, order=return_object, products=products), error_code

@page.route('/panier/add', methods=['POST'])
def add_to_panier():
    data = request.get_json()
    product = data.get('product', {})
    id = product.get('id', {})
    quantity = product.get('quantity', {})
    print(product)
    status = add_product_to_cart(id, quantity)
    if status:
        return {"localisation": "http://127.0.0.1:5000/page/panier"}
    else:
        return {"errors": 404}
    
@page.before_request
def before_request():
    cart_id = request.cookies.get('cart_id')
    if not cart_id:
        cart_id = str(uuid.uuid4())
        set_panier_redis(cart_id)
        g.set_cookie = True
    g.cart_id = cart_id

@page.after_request
def after_request(response):
    if getattr(g, 'set_cookie', False):
        response.set_cookie('cart_id', g.cart_id, max_age=3600, httponly=True)
    return response