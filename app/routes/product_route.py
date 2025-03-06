from flask import Blueprint

from app.controllers.product_controller import ProductController

products = Blueprint('products', __name__, url_prefix='/products')

@products.route('/')
def get_products():
    return ProductController.get_products()

@products.route('/<int:product_id>')
def get_product(product_id: int):
    product = ProductController.get_product_by_id(product_id)
    return product.to_dict()