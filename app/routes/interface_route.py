from flask import Blueprint, render_template, request, g, redirect, url_for

import os
from app.controllers.product_controller import ProductController
from app.controllers.order_controller import OrderController
import uuid
from redis import Redis
from rq import Queue
from app.helper.panier_helper import get_panier_redis, add_product_to_cart, set_panier_redis
DB_REDIS = os.getenv('REDIS')
DB_REDIS_PORT = os.getenv('REDIS_PORT')
redis_url = f"redis://{DB_REDIS}:{DB_REDIS_PORT}/0"
redis = Redis.from_url(redis_url)

queue = Queue(connection=redis)
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

@page.route('/panier', methods=['POST'])
def process_panier():
    products = get_panier_redis()
    dict_products: list = []
    for product in products:
        dict_products.append({"id": product.id, "quantity": product.quantity})
    return_object, error_code = OrderController.process_order(dict_products)
    print(error_code)
    if error_code == 201 or error_code == 200:
        return redirect(url_for('page.shipping_form',  id=return_object['order_id']))
    else:
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
    if error_code == 302:
        products = [
            {
                "id": link.product.id,
                "name": link.product.name,
                "price": link.product.price,
                "quantity": link.quantity
            }
            for link in return_object.product_links
        ]
        return render_template('confirmation.html', id=id, order=return_object, products=products), error_code
    else:
        return render_template('error.html', errors=return_object, error_code=error_code)

@page.route('/process/<string:job_id>', methods=['GET'])
def process(job_id: str):
    job = queue.fetch_job(job_id)
    if job and not job.is_finished:
        return render_template('processing.html'), 202
    else:
        print(job.return_value())
        result, error_code = job.return_value()
        return redirect(url_for('page.confirmation',  id=result['id']))

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