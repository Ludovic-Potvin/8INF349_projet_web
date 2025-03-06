import json

import logging.config
import os

from app import create_app
from app.database import init_db

app = create_app()

init_db()

if __name__ == '__main__':
    app.run(use_reloader=False)