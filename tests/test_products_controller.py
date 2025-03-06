from difflib import restore

from app.controllers.product_controller import ProductController

class TestProductController:

    def test_get_product(self):
        response = ProductController.get_products()
        list_of_products = response.json()
        assert response.status_code == 200
        assert len(list_of_products) > 0

    def test_get_valid_id_product(self):
        response = ProductController.get_product_by_id(1)
        product = response.json()
        assert response.status_code == 200
        assert product is not None
        assert product['id'] == 1

    def test_get_invalid_id_product(self):
        response = ProductController.get_product_by_id(51)
        invalid_product = response.json().get('error')
        assert response.status_code == 404
        assert invalid_product == f"Product {51} not found"


