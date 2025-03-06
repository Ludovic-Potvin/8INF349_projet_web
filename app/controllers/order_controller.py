import app
from app.controllers.product_controller import ProductController
from app.database import Session
from flask import abort, url_for

from app.models.order import Order


class OrderController():

    @classmethod
    def process_order(cls, data):
        app.logger.info("Entered process_order")
        print("Entered process_order")
        error_code = 200
        return_object = {"message": "Commande traitée avec succès"}

        product = data.get('product', {})
        id = product.get('id', {})
        quantity = product.get('quantity', {})
        
        if product and id and quantity and quantity >= 1 :
            app.logger.info(f"Try to get product #{id} in database")
            print(f"Try to get product #{id} in database")
            product = ProductController.get_product_by_id(id)
            print("Fetch cleared")
            if product and quantity <= product.in_stock:
                print("Product in stock")
                return_object, error_code = OrderController._saveorder(product, quantity)
            else:
                app.logger.error("Product not in stock")
                print("Product not in database")
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
            app.logger.error("No product sent")
            print("No product sent")
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
    
    @classmethod
    def get_order(cls, order_id: int):
        app.logger.info("Entered get_order")
        print("Entered get_order")
        with Session() as session:
            try:
                order = session.query(Order).filter(Order.id == order_id).first()
                error_code = 302
                if order is None:
                    abort(404, f"Order {order_id} not found")
                    print(f"Order {order_id} not found")
            except Exception as e:
                app.logger.error(f"An error occurred: {str(e)}")
                abort(500, "An unexpected server error happened")
            finally:
                session.close()
        return order, error_code
    
    @classmethod
    def _saveorder(cls, product, quantity_ordered):
        app.logger.info("Entered save_order")
        print("Entered save_order")
        with Session() as session:
            try:
                # Création de la commande
                new_order = Order(
                    product_id=product.id,
                    quantity = quantity_ordered
                )

                # Mise à jour du stock du produit
                product.in_stock -= quantity_ordered

                # Sauvegarde dans la base de données
                session.add(product)
                session.add(new_order)
                session.commit()

                app.logger.info(f"Commande enregistrée avec succès : {new_order.id}")
                location = url_for('order.get_order', order_id=new_order.id, _external=True)
                return_object = "Location : " + location
                error_code = 201
            except Exception as e:
                app.logger.error(f"An error occurred: {str(e)}")
                abort(500, "An unexpected server error happened")
            finally:
                session.close()
        return return_object, error_code