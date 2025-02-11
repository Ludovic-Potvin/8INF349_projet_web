import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'data.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SOURCE_API_URL = "https://dimensweb.uqac.ca/~jgnault/shops/products/"