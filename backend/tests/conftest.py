import pytest
from main import create_app
from config import TestConfig
from extensions import db

@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

        yield app
        

@pytest.fixture
def client(app):
    return app.test_client()