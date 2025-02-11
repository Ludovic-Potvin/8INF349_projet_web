from flask import Flask
from config import Config

def create_app():
    # Load app config
    app = Flask(__name__)
    app.config.from_object(Config)

    return app