from time import process_time_ns

import app
import os
import re
from app.controllers.product_controller import ProductController
from flask import abort
from app.database import Session
from flask import abort, url_for, jsonify
import json
import requests
import app
from app.models.order import Order
from app.models.order_product import OrderProduct
from app.models.shipping_information import ShippingInformation
from app.models.credit_card import CreditCard
from redis import Redis
from rq import Queue, Worker
from sqlalchemy import text
from rq import Queue
from redis import Redis
import requests



DB_REDIS = os.getenv('REDIS')
DB_REDIS_PORT = os.getenv('REDIS_PORT')

redis_url = f"redis://{DB_REDIS}:{DB_REDIS_PORT}/0"
redis = Redis.from_url(redis_url)

queue = Queue(connection=redis)


def this_is_a_test2(this_number):
    for i in range(this_number):
        print("asl")

def this_is_a_test1(credit_card, total):
    response = OrderController.make_payment(credit_card, total)
    for i in range(1001):
        print(response)
    return "asd"

def make_payment(credit_card_information, amount_charged):
    url = "https://dimensweb.uqac.ca/~jgnault/shops/pay/"
    payload = {
        "credit_card": credit_card_information,
        "amount_charged": amount_charged
    }
    response = requests.post(url, json=payload)
    return response

class OrderController:
    @classmethod
    def process_order(cls, products):
        app.logger.info("Entered process_order")
        print("Entered process_order")
        error_code = 200
        return_object = {"message": "Commande traitée avec succès"}

        if products:
            if cls._check_products_in_bd(products):
                if cls._check_inventory(products):
                    return_object, error_code = cls._saveorder(products, return_object, error_code)
                else:
                    app.logger.error("Product not in stock")
                    print("Product not in stock")
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
    def _check_products_in_bd(cls, products):
        app.logger.info("Entered _check_products_in_bd")
        print("Entered _check_products_in_bd")
        for item in products:
            id = item.get('id', {})
            app.logger.info(f"Try to get product #{id} in database")
            print(f"Try to get product #{id} in database")
            product = ProductController.get_product_by_id(id)
            if not product:
                return False
        return True

    @classmethod
    def _check_inventory(cls, products):
        app.logger.info("Entered _check_inventory")
        print("Entered _check_inventory")
        for item in products:
            id = item.get('id', {})
            app.logger.info(f"Try to get product #{id} in database")
            print(f"Try to get product #{id} in database")
            product = ProductController.get_product_by_id(id)
            if not item['quantity'] or item['quantity'] > product.in_stock:
                return False
        return True

    @classmethod
    def get_order(cls, order_id: int):
        #Check if the order is in redis
        #cached_order = redis.get(order_id)
        #if cached_order:
            #return cached_order

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
                else: 
                    abort(500, "An unexpected server error happened")
            finally:
                session.close()

        if order.paid:
            redis.set(order_id, json.dumps(order.to_dict()))
        return order, error_code
    
    @classmethod
    def _saveorder(cls, products, return_object, error_code):
        app.logger.info("Entered save_order")
        with Session() as session:
            price = 0
            weight = 0

            for item in products:               
                product = ProductController.get_product_by_id(item['id'])
                price += product.price * item['quantity']
                weight += product.weight * item['quantity']

                product.in_stock -= item['quantity']
                session.add(product)

            if weight < 500:
                shipping = 5
            elif weight > 500 and weight > 2000:
                shipping = 10
            else:
                shipping = 25

            try:
                new_order = Order(
                    total_price = price,
                    shipping_price = shipping
                )
                session.add(new_order)
                session.flush()

                for item in products:
                    order_product = OrderProduct(
                        order_id=new_order.id,
                        product_id=item['id'],
                        quantity=item['quantity']
                    )
                    session.add(order_product)

                session.commit()
                app.logger.info(f"Commande enregistrée avec succès : {new_order.id}")

                return_object =  {"order_id": new_order.id}
                error_code = 201
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                app.logger.error(f"An error occurred: {str(e)}")
                abort(500, "An unexpected server error happened")
            finally:
                session.close()
        return return_object, error_code
    
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
            return self.update_order_card_before(id, data)
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
            tax = {
                "QC" : order.total_price * 1.15,
                "ON" : order.total_price * 1.13,
                "AB" : order.total_price * 1.05,
                "BC" : order.total_price * 1.12,
                "NS" : order.total_price * 1.14
            }
            with Session() as session:
                try:
                    order.total_price_tax = tax[shipping_data.get("province")]
                    if order.shipping_info:
                        order.shipping_info.country = shipping_data.get("country")
                        order.shipping_info.address = shipping_data.get("address")
                        order.shipping_info.postal_code = shipping_data.get("postal_code")
                        order.shipping_info.city = shipping_data.get("city")
                        order.shipping_info.province = shipping_data.get("province")
                    else:
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
                    return_object = order.to_dict()
                except Exception as e:
                    app.logger.error(f"An error occurred: {str(e)}")
                    abort(500, "An unexpected server error happened")
                finally:
                    session.close()
        return return_object, error_code
    
    #Description: Only update the credit card info
    @classmethod
    def update_order_card_before(self, id, data):
        order, error_code = self.get_order(id)

       #If the order is not in the cache, it is not paid...
        cached_order = redis.get(id)
        if cached_order:
            error_code = 409
            return_object = {
                "errors": {
                    "order": {
                        "code": "processing",
                        "name": "La transaction est déjà en cours de paiement"
                        }
                    }
                }
            return return_object, error_code
    
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
            return return_object, error_code
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
            return return_object, error_code
        if order.paid:
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
            return return_object, error_code

        total = order.total_price_tax + order.shipping_price
        job = queue.enqueue(update_order_card_after, id, credit_card, total)


        return self.verify_payment(job.id)

    @classmethod
    def verify_payment(self, job_id):
        error_code = 202
        return_object = {"location": url_for('page.process', job_id=job_id)}
        return return_object, error_code


def update_order_card_after(id, credit_card, total):
    order, error_code = OrderController.get_order(id)
    response = make_payment(credit_card, int(total))

    if response.status_code != 200:
        return response.json, response.status_code
    with Session() as session:
        try:
            if order.creditCard:
                order.creditCard.name = credit_card.get("name")
                order.creditCard.number = credit_card.get("number").replace(" ", "")[:12]
                order.creditCard.expiration_year = credit_card.get("expiration_year")
                order.creditCard.cvv = credit_card.get("cvv")
                order.creditCard.exp_month = credit_card.get("exp_month")
            else:
                # If the credit card doesn't exist, create a new one
                credit_card = CreditCard(
                    name=credit_card['name'],
                    number=credit_card['number'].replace(" ", "")[:12],
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
            return_object = order.to_dict()

            #redis.set(order.id, json.dumps(return_object))
        finally:
            session.close()
    return return_object, error_code
