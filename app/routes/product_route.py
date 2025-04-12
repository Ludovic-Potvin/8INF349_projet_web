from flask import Blueprint, render_template

from app.controllers.product_controller import ProductController

products = Blueprint('products', __name__, url_prefix='/products')

@products.route('/')
def get_products():
    products = ProductController.get_products()
    #return products
    return render_template('products.html', products=products)

@products.route('/<int:product_id>')
def get_product(product_id: int):
    product = ProductController.get_product_by_id(product_id)
    return render_template('product.html', product=product)

@products.route('/api/<int:product_id>')
def get_product_api(product_id: int):
    product = ProductController.get_product_by_id(product_id)
    return product.to_dict()