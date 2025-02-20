from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from .models.products import Product
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

def _fetch_inital_data():
    """Fetch product data from the API using urllib."""
    try:
        with urllib.request.urlopen(Config.SOURCE_API_URL) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

#Had some trouble with the convertion of the db result to json
#Here are the link that I used to fix the problem
#https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
#https://www.geeksforgeeks.org/python-convert-a-list-to-dictionary/
#https://www.geeksforgeeks.org/how-to-convert-python-dictionary-to-json/
#https://stackoverflow.com/questions/1545050/python-one-line-for-expression
#https://www.digitalocean.com/community/tutorials/python-pretty-print-json --> For this I noticed that the "pretty" change will nots be displayed in the brows
def get_products():
    db_session = Session()
    products = db_session.query(Product).all()

    products_list = []
    for product in products:
        products_list.append(product.as_dict())

    #This will also work but I don't find it clear enough
    #products_list = [product.as_dict() for product in products]
    #for product in products: products_list.append(product.as_dict())

    db_session.close()
    return products_list

def get_product(product_id):
    db_session = Session()
    product = db_session.query(Product).get(product_id)

    if product is None:
        return None

    db_session.close()
    return product.as_dict()