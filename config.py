import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'data.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SOURCE_API_URL = "https://dimensweb.uqac.ca/~jgnault/shops/products/"
    LOGGER_CONFIG_FILE = os.path.join(basedir, 'logging', 'config.json')
    LOG_DIR = os.path.join(basedir, 'logs')
