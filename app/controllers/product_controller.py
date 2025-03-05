from flask import abort, jsonify, Response

import app
from app.database import Session
from app.models.product import Product


class ProductController(object):

    @classmethod
    def get_product(cls, product_id: int):
        """Return a single product by id"""
        with Session() as session:
            try:
                product = session.query(Product).filter(Product.id == product_id).first()
                if product is None:
                    abort(404, "Product not found")
            except Exception as e:
                app.logger.error(f"An error occurred: {str(e)}")
                abort(404, "Product not found")
            finally:
                session.close()

        return product.to_dict()

