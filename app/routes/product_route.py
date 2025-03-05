from flask import Blueprint

from app.controllers.product_controller import ProductController

products = Blueprint('products', __name__, url_prefix='/products')

@products.route('/<int:product_id>')
def get_products(product_id: int):
    return ProductController.get_product(product_id)