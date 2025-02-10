from flask import Flask
from sqlalchemy import SQLAlchemy
from config import Config

# Init SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Load app config
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup database

    # Connect database to the app
    db.init_app(app)

    return app