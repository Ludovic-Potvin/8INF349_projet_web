from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from .models.Order import Order
from .models.Shipping_information import ShippingInformation
from .models.product import Product
from .models.CreditCard import CreditCard
import urllib.request
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
