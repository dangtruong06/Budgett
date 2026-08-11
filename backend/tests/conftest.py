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

@pytest.fixture
def auth_headers(client):
    client.post('/api/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    token = response.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}

# register new user to try and access other's resources
@pytest.fixture
def other_auth_headers(client):
    client.post('/api/register', json={
        'email': 'test2@example.com',
        'password': 'password123'
    })

    response = client.post('/api/login', json={
        'email': 'test2@example.com',
        'password': 'password123'
    })

    token = response.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}
