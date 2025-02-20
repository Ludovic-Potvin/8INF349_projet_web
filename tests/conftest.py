import pytest
from app.database import engine, init_db
from app.models.base import Base
from app import create_app

@pytest.fixture(scope="function")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,  # Enable testing mode
    })
    with app.app_context():
        # Recreate the database before each test
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        init_db()
    yield app

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
