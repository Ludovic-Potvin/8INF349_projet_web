import json
from http.client import responses

from app.controllers.order_controller import OrderController
from app.controllers.product_controller import ProductController
from config import Config

import os
from app.database import init_db

class TestProductController:

    @staticmethod
    def generate_order(product_id, quantity):
        return {
            "product": {
                "id" : product_id,
                "quantity" : quantity
            }
        }

    @staticmethod
    def reset_database():
        os.remove(Config.SQLALCHEMY_DATABASE_LOCATION)
        init_db()

    @classmethod
    def setup_class(cls):
        # This code runs once before any test methods in this class
        cls.reset_database()

    def test_valid_post_order(self):
        product_before_order = ProductController.get_product_by_id(1)
        response = OrderController.process_order(self.generate_order(1, 1))
        assert response[1] == 201
        product_after_order = ProductController.get_product_by_id(1)
        assert product_before_order.in_stock != product_after_order.in_stock
        order, status_code = OrderController.get_order(1)
        assert status_code == 302
        assert order.product_id == 1
        assert order.id == 1
        assert order.quantity == 1

    def test_out_of_stock_post_order(self):
        response1 = OrderController.process_order(self.generate_order(1,1))
        response2 = OrderController.process_order(self.generate_order(1,1))
        assert response2[1] == 422
        assert "Out-of-inventory" in response2[0]["errors"]["product"]["code"]

    def test_missing_field_post_order(self):
        response = OrderController.process_order(self.generate_order('',''))
        assert response[1] == 422
        assert "Missing-fields" in response[0]["errors"]["product"]["code"]