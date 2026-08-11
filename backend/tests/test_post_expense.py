# test create expense routes - POST
def test_create_expense_no_auth(client):
    response = client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-08-12',
    })

    assert response.status_code == 401

def test_create_expense(client, auth_headers):
    response = client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-08-12',
    },
    headers=auth_headers)

    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Pho'
    assert data['category'] == 'Food'
    assert data['amount'] == 30.4
    assert data['expense_date'] == '2025-08-12'
    assert 'id' in data

def test_create_expense_missing_name(client, auth_headers):
    response = client.post('/api/expenses', json={
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-08-12',
    },
    headers=auth_headers)

    assert response.status_code == 400
    assert response.get_json() == {'error': 'missing required fields'}

def test_create_expense_missing_category(client, auth_headers):
    response = client.post('/api/expenses', json={
        'name': 'Pho',
        'amount': 30.4,
        'expense_date': '2025-08-12',
    },
    headers=auth_headers)

    assert response.status_code == 400
    assert response.get_json() == {'error': 'missing required fields'}

def test_create_expense_missing_amount(client, auth_headers):
    response = client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'expense_date': '2025-08-12',
    },
    headers=auth_headers)

    assert response.status_code == 400
    assert response.get_json() == {'error': 'missing required fields'}

def test_create_expense_missing_date(client, auth_headers):
    response = client.post('/api/expenses', json={
        'name': 'Pho',
        'amount': 30.4,
        'category': 'Food',
    },
    headers=auth_headers)

    assert response.status_code == 400
    assert response.get_json() == {'error': 'missing required fields'}

def test_create_expense_invalid_format(client, auth_headers):
    response = client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'amount': 'one hundred',
        'expense_date': '2025-08-12',
    },
    headers=auth_headers)

    assert response.status_code == 400
    assert response.get_json() == {'error': 'invalid amount or date format'}
