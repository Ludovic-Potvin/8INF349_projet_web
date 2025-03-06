import app
from app.controllers.product_controller import ProductController
from app.database import Session
from flask import abort

from app.models.order import Order


class OrderController():

    @classmethod
    def process_order(cls, data):
        app.logger.info("Entered process_order")
        error_code = 200
        return_object = {"message": "Commande traitée avec succès"}

        product = data.get('product', {})
        id = product.get('id', {})
        quantity = product.get('quantity', {})
        
        if product and id and quantity and quantity >= 1 :
            product = ProductController.get_product_by_id(id)
            if product and quantity <= product.in_stock:
                OrderController._saveorder(product, quantity)
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
    
    @classmethod
    def get_order(cls, order_id: int):
        app.logger.info("Entered get_order")
        with Session() as session:
            try:
                order = session.query(Order).filter(Order.id == order_id).first()
                if order is None:
                    abort(404, f"Order {order_id} not found")
            except Exception as e:
                app.logger.error(f"An error occurred: {str(e)}")
                abort(500, "An unexpected server error happened")
            finally:
                session.close()
        return order.to_dict()
    
    @classmethod
    def _saveorder(product, quantity_ordered):
            app.logger.info("Entered save_order")
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
                    session.add(new_order)
                    session.commit()

                    app.logger.info(f"Commande enregistrée avec succès : {new_order.id}")
                except Exception as e:
                    app.logger.error(f"An error occurred: {str(e)}")
                    abort(500, "An unexpected server error happened")
                finally:
                    session.close()