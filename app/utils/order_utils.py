import os
import json
import requests
from app.models.order import Order
from app.models.order_product import OrderProduct
from app.controllers.product_controller import *
from app.models.shipping_information import ShippingInformation
from app.models.credit_card import CreditCard
PAYMENT_URL = os.getenv('PAYMENT_URL')


@staticmethod
def make_payment(credit_card_information, amount_charged):
    url = PAYMENT_URL
    payload = {
        "credit_card": credit_card_information,
        "amount_charged": amount_charged
    }
    response = requests.post(url, json=payload)
    return response

@staticmethod
def order_to_object(data):
    order_data = json.loads(data)
    shipping_data = order_data["shipping_info"]
    credit_card_data = order_data["credit_card"]
    products_data = order_data["products"]
    order_products_informations = []
    for item in products_data:
        temp = OrderProduct(
            product_id=item['product_id'],
            quantity=item['quantity'],
        )
        temp.product = ProductController.get_product_by_id(item['product_id'])
        order_products_informations.append(temp)
    credit_card_informations = CreditCard(
        name=credit_card_data.get('name'),
        number=credit_card_data.get('number'),
        expiration_year=credit_card_data.get('expiration_year'),
        exp_month=credit_card_data.get('exp_month'),
    )
    shipping_informations = ShippingInformation(
        id=shipping_data.get('id'),
        country=shipping_data.get('country'),
        address=shipping_data.get('address'),
        postal_code=shipping_data.get('postal_code'),
        city=shipping_data.get('city'),
        province=shipping_data.get('province'),
    )
    order = Order(
        email=order_data.get('email'),
        total_price=order_data.get('total_price'),
        id=order_data.get('id'),
        total_price_tax=order_data.get('total_price_tax'),
        transaction=order_data.get('transaction'),
        paid=order_data.get('paid'),
        shipping_price=order_data.get('shipping_price'),
        product_links=order_products_informations,
        shipping_info=shipping_informations,
        creditCard=credit_card_informations,
    )
    return order