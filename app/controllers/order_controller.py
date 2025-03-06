from app.database import retrieve_product

class OrderController():

    @classmethod
    def process_order(data):
        product = data.get('product', {})
        id = product.get('id', {})
        quantity = product.get('quantity', {})
        
        if product and id and quantity and quantity >= 1 :
            product = retrieve_product(id)
            if product and quantity <= product.in_stock:
                #save order here
            else:
                error_code = 422
                return_object = {
                                    "errors" : {
                                        "product": {
                                            "code": "Out-of-inventory",
                                            "name": "Le produit demandé n'est pas en inventaire"
                                        }
                                    }
                                }
        else:
            error_code = 422
            return_object = {
                                "errors" : {
                                    "product": {
                                        "code": "Missing-fields",
                                        "name": "La création d'une commande nécessite un produit"
                                    }
                                }
                            }
        return return_object, error_code