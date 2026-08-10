# register tests
def test_register(client):
    response = client.post('/api/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    assert response.status_code == 201
    assert response.get_json() == {'success': 'new user created'}


def test_register_duplicate(client):
    client.post('/api/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/api/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    assert response.status_code == 409
    assert response.get_json() == {'error': 'email already exists'}

def test_empty_register_email(client):
    response = client.post('/api/register', json={
        'email': '',
        'password': 'some-password'
    })

    assert response.status_code == 400
    assert response.get_json() == {"error": "empty email or password"}

def test_empty_register_password(client):
    response = client.post('/api/register', json={
        'email': 'test@example.com',
        'password': ''
    })

    assert response.status_code == 400
    assert response.get_json() == {"error": "empty email or password"}

# login tests
def test_login(client):
    client.post('/api/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_wrong_password(client):
    client.post('/api/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
        
    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })

    assert response.status_code == 401
    assert response.get_json() == {'error': 'unauthorized'}

def test_login_nonexistent_email(client):
    response = client.post('/api/login', json={
        'email': 'nobody@example.com',
        'password': 'whatever'
    })

    assert response.status_code == 401
    assert response.get_json() == {'error': 'unauthorized'}