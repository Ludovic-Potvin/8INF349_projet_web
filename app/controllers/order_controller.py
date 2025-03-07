import app
from app.controllers.product_controller import ProductController
from flask import abort
from app.database import Session
from flask import abort, url_for, jsonify

from app.models.order import Order
from app.models.Shipping_information import ShippingInformation
from app.models.CreditCard import CreditCard

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
                print(f"Paid: {order.paid}")
                print(f"Shipping Info: {order.shipping_info}")
                print(f"Card Info: {order.creditCard}")
                error_code = 302
                if order is None:
                    print(f"Order {order_id} not found")
                    abort(404)
            except Exception as e:
                app.logger.error(f"An error occurred: {str(e)}") 
                if order is None:
                    print(f"Order {order_id} not found")
                    abort(404, f"Order {order_id} not found")
                else: abort(500, "An unexpected server error happened")
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
    
    #======== PUT ========
    # Description: Redirect to the correct function
    @classmethod
    def update(self, id, data):
        app.logger.info("Entered update")
        print("Entered update")
        if 'order' in data and 'credit_card' in data:
            return abort(400, {"errors": {
                        "order": {
                            "code": "Bad Request",
                            "name": "Un seul type d'information peut être modifier à la fois"
                            }
                        }
                    })

        if 'order' in data:
            return self.update_order_shipping(id, data)
        elif 'credit_card' in data:
            return self.update_order_card(id, data)
        else:
            return abort(418, {"error": "tea - how did you end up here"})

    # Description: Only update the shipping info and the email
    @classmethod
    def update_order_shipping(self, id, data):
        app.logger.info("update_order_shipping")
        order, error_code = self.get_order(id)
        order_data = data.get('order')
        if not order_data:
            print("No order data")
            error_code = 422
            return_object = {"errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Il manque un ou plusieurs champs qui sont obligatoires",
                    }
                }
            }
        
        email = order_data.get('email')
        shipping_data = order_data.get('shipping_information')
        
        if shipping_data is None or  email is None:
            print("missing-fields")
            error_code = 422
            return_object = {
                "errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Il manque un ou plusieurs champs qui sont obligatoires",
                    }
                }
            }

        required_fields = ['country', 'address', 'postal_code', 'city', 'province']
        missing_fields = [field for field in required_fields if not shipping_data.get(field)]

        if missing_fields:
            print("missing-fields")
            error_code = 422
            return_object = {
                "errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Il manque un ou plusieurs champs qui sont obligatoires",
                    }
                }
            }

        if(error_code == 302):
            with Session() as session:
                try:
                    order.email = email
                    if order.shipping_info:
                        print("Updating")
                        order.shipping_info.country = shipping_data.get("country")
                        order.shipping_info.address = shipping_data.get("address")
                        order.shipping_info.postal_code = shipping_data.get("postal_code")
                        order.shipping_info.city = shipping_data.get("city")
                        order.shipping_info.province = shipping_data.get("province")
                        print("Updated")
                    else:
                        print("Adding")
                        new_shipping_info = ShippingInformation(
                            country=shipping_data.get("country"),
                            address=shipping_data.get("address"),
                            postal_code=shipping_data.get("postal_code"),
                            city=shipping_data.get("city"),
                            province=shipping_data.get("province"),
                            order_id=order.id
                        )
                        session.add(new_shipping_info)

                    session.add(instance=order)
                    session.commit()
                    error_code = 200
                    return_object = jsonify(order.to_dict())
                except Exception as e:
                    app.logger.error(f"An error occurred: {str(e)}")
                    abort(500, "An unexpected server error happened")
                finally:
                    session.close()
        print(error_code)
        return return_object, error_code
    
    #Description: Only update the credit card info
    @classmethod
    def update_order_card(self, id, data):
        app.logger.info("update_order_card")
        order, error_code = self.get_order(id)

        credit_card = data.get('credit_card')
        if not credit_card:
            app.logger.info("missing card")
            error_code = 422
            return_object = {
                "errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Les informations du client sont nécessaire avant d'appliquer une carte de crédit"
                        }
                    }
                }
        required_fields = ['name', 'number', 'expiration_year', 'cvv', 'expiration_month']
        missing_fields = [field for field in required_fields if not credit_card.get(field)]
        if missing_fields:
            app.logger.info("missing field")
            error_code = 422
            return_object = {
                "errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Les informations du client sont nécessaire avant d'appliquer une carte de crédit"
                        }
                    }
                }
        if order.paid is True:
            app.logger.info("already paid")
            error_code = 422
            return_object = {
                "errors" : {
                    "order": {
                        "code": "already-paid",
                        "name": "La commande a déjà été payée."
                    }
                }
            }

        if(error_code == 302):
            #TO DO SEND CREDIT CARDS INFO TO SERVICE
            # if error:
                #return msg
            with Session() as session:
                try:
                    if order.creditCard:
                        order.creditCard.name = credit_card.get("name")
                        order.creditCard.number = credit_card.get("number")
                        order.creditCard.expiration_year = credit_card.get("expiration_year")
                        order.creditCard.cvv = credit_card.get("cvv")
                        order.creditCard.exp_month = credit_card.get("exp_month")
                    else:
                        # If the credit card doesn't exist, create a new one
                        credit_card = CreditCard(
                            name=credit_card['name'],
                            number=credit_card['number'],
                            expiration_year=credit_card['expiration_year'],
                            cvv=credit_card['cvv'],
                            exp_month=credit_card['expiration_month'],
                            order_id=order.id
                        )
                        session.add(credit_card)

                    order.paid = True
                    session.add(instance=order)
                    session.commit()
                    app.logger.info("update_order_card did")
                    error_code = 200
                    return_object = jsonify(order.to_dict())
                finally:
                    session.close()
        return return_object, error_code


