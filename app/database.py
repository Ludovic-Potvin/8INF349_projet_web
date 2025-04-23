import os
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from app.models.order import Order
from app.models.shipping_information import ShippingInformation
from app.models.products import Product
import urllib.request
from app.models.base import Base
import json

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create engine
engine = create_engine(DATABASE_URL)

# Create Session
Session = sessionmaker(bind=engine)

def init_db():
    """Create tables and populate database if needed."""
    Base.metadata.create_all(bind=engine)

    with Session() as session:
        try:
            if not session.query(Product).first():
                _populate_db(session)
                session.commit()
            if not session.query(Order).first():
                _populate_order(session)                
            else:
                print("Using existing database")

        except Exception as e:
            print(f"Failed to populate database: {e}")
        finally:
            session.close()


def _populate_db(session):
    data = _fetch_initial_data()
    try:
        for product in data.get('products', []):
            sanitized_product = _sanitize_product(product)
            new_product = Product(**sanitized_product)
            session.add(new_product)
    except TypeError as e:
        print(f"Failed to populate database, a key is missing: {e}")


def _fetch_initial_data() -> dict:
    """Fetch product data from the API using urllib."""
    try:
        with urllib.request.urlopen(Config.SOURCE_API_URL) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {}

def _sanitize_product(product):
    sanitized_product = product

    # description
    sanitized_product['description'] = re.sub(
        r'[\x00-\x1F\x7F]', '', product['description'])

    # in_stock
    sanitized_product['in_stock'] = 50 if product['in_stock'] else 0

    return sanitized_product

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
    shipping_info = new_shipping_info,
    )
    session.add(new_order)
    session.commit()
