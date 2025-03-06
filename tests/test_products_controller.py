from app.controllers.product_controller import ProductController

class TestProductController:

    def test_get_product(self):
        list_of_products = ProductController.get_products()
        #assert response.status_code == 200
        assert len(list_of_products) > 0

    def test_get_valid_id_product(self):
        product = (ProductController.get_product_by_id(1)).to_dict()
        #assert response.status_code == 200
        assert product is not None
        assert product['id'] == 1

    #def test_get_invalid_id_product(self):
    #    response = ProductController.get_product_by_id(51)
    #    assert response.status_code == 404
    #    assert response == f"Product {51} not found"


