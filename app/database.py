from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from .models.Order import Order
from .models.Shipping_information import ShippingInformation
from .models.product import Product
from .models.CreditCard import CreditCard
import urllib.request
from sqlalchemy.ext.declarative import declarative_base
from app.models.base import Base
import json


# Create engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Create Session
Session = sessionmaker(bind=engine)

def init_db():
    """Create tables and populate database if needed."""
    Base.metadata.create_all(bind=engine)

    db_session = Session()
    # Check if database is already populated
    if db_session.query(Product).first() is None:
        _populate_db(db_session)
        print("Database created and populated")
    elif db_session.query(Order).first() is None:
        _populate_order(db_session)
    else:
        print("Using existing database")

    db_session.close()

def _populate_db(session):
    data = _fetch_inital_data()

    if data.get("products"):
        for item in data.get('products'):
            new_product = Product(
                name=item['name'],
                description=item['description'],
                in_stock=item['in_stock'],
                price=item['price'],
                weight=item['weight'],
                image=item['image']
            )
            session.add(new_product)

        session.commit()

def _populate_order(session):
    new_shipping_info = ShippingInformation(
        country='Canada',
        address='201, rue Président-Kennedy',
        postal_code='G7X 3Y7',
        city='Chicoutimi',
        province='QC'
    )
    new_order = Order(
    email="customer@example.com",
    total_price=200,
    total_price_tax=20,
    transaction="txn_123456",
    paid=True,
    shipping_price=10,
    product_id=1,
    shipping_info = new_shipping_info,
    )
    session.add(new_order)
    session.commit()


def _fetch_inital_data():
    """Fetch product data from the API using urllib."""
    try:
        with urllib.request.urlopen(Config.SOURCE_API_URL) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

#======== PUT ========
# Description: Only update the shipping info and the email
def update_order_shipping(id, data):
    db_session = Session()

    order = db_session.query(Order).get(id)
    if not order:
        return jsonify({"error": f"Order {id} not found"}), 404

    order_data = data.get('order')
    if not order_data:
        return jsonify({
            "errors": {
                "order": {
                    "code": "missing-fields",
                    "name": "Il manque un ou plusieurs champs qui sont obligatoires",
                }
            }
        }), 422
    
    email = order_data.get('email')
    shipping_data = order_data.get('shipping_information')
    
    if shipping_data is None or  email is None:
        return jsonify({
            "errors": {
                "order": {
                    "code": "missing-fields",
                    "name": "Il manque un ou plusieurs champs qui sont obligatoires",
                }
            }
        }), 422

    required_fields = ['country', 'address', 'postal_code', 'city', 'province']
    missing_fields = [field for field in required_fields if not shipping_data.get(field)]

    if missing_fields:
        return jsonify({
            "errors": {
                "order": {
                    "code": "missing-fields",
                    "name": "Il manque un ou plusieurs champs qui sont obligatoires",
                }
            }
        }), 422

    order.email = email
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
        db_session.add(new_shipping_info)

    db_session.commit()
    return jsonify(order.to_dict()), 200

#Description: Only update the credit card info
def update_order_card(id, data):
    db_session = Session()

    order = db_session.query(Order).get(id)
    if not order:
        return jsonify({"error": f"Order {id} not found"}), 404
    else:
        credit_card = data.get('credit_card')
        if not credit_card:
            return jsonify({
                "errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Les informations du client sont nécessaire avant d'appliquer une carte de crédit"
                        }
                    }
                }), 422
        required_fields = ['name', 'number', 'expiration_year', 'cvv', 'expiration_month']
        missing_fields = [field for field in required_fields if not credit_card.get(field)]
        if missing_fields:
            return jsonify({
                "errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Les informations du client sont nécessaire avant d'appliquer une carte de crédit"
                        }
                    }
                }), 422
        
        if order.paid is True:
            return {
                "errors" : {
                    "order": {
                        "code": "already-paid",
                        "name": "La commande a déjà été payée."
                    }
                }
            }, 422

        #TO DO SEND CREDIT CARDS INFO TO SERVICE
        # if error:
            #return msg

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
            db_session.add(credit_card)

        order.paid = True
        db_session.commit()
        return jsonify(order.to_dict()), 200
