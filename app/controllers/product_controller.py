from http.client import HTTPException

from flask import abort

import app
from app.database import Session
from app.models.products import Product


class ProductController(object):

    @classmethod
    def get_products(cls):
        """Return a list of products"""
        with Session() as session:
            try:
                products = session.query(Product).all()
                print(products)
                if products is None:
                    abort(404)
                products_list = []
                for product in products:
                    products_list.append(product.to_dict())
                #The following code will also work but I don't find it clear enough.
                #To see how this was done, look at the documentation.
                #products_list = [product.as_dict() for product in products]
                #for product in products: products_list.append(product.as_dict())
            except Exception as e:
                app.logger.error(f"An error occurred: {str(e)}")
                if "404" in str(e):
                    abort(404, message="No products were found")
                else:
                    abort(500, "An unexpected server error happened")
            finally:
                session.close()
        return products_list

    @classmethod
    def get_product_by_id(cls, product_id: int):
        """Return a single product by id"""
        with Session() as session:
            try:
                product = session.query(Product).filter(Product.id == product_id).first()
                if product is None:
                    abort(404)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                app.logger.error(f"An error occurred: {str(e)}")
                if "404" in str(e):
                    abort(404, f"Product {product_id} not found")
                else:
                    abort(500, "An unexpected server error happened")
            finally:
                session.close()

        return product.to_dict()

