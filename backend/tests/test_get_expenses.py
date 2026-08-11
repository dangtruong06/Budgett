# test get expenses - GET
def test_get_single_expense_wrong_user(client, auth_headers, other_auth_headers):
    # user A creates an expense
    create_response = client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-08-12',
    }, headers=auth_headers)
    expense_id = create_response.get_json()['id']

    # user B access user A's resource
    response = client.get(f'/api/expenses/{expense_id}', headers=other_auth_headers)
    assert response.status_code == 403
    assert response.get_json() == {'error': 'Forbidden'}

def test_get_single_expense(client, auth_headers):
    create_response = client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-08-12',
    }, headers=auth_headers)
    expense_id = create_response.get_json()['id']

    response = client.get(f'/api/expenses/{expense_id}', headers=auth_headers)
    assert response.status_code == 200
    assert 'id' in response.get_json()

def test_get_single_expense_not_found(client, auth_headers):
    response = client.get('/api/expenses/9999', headers=auth_headers)
    assert response.status_code == 404

def test_get_all_expenses(client, auth_headers):
    client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-02-06',
    }, headers=auth_headers)

    client.post('/api/expenses', json={
        'name': 'Monitor',
        'category': 'Personal',
        'amount': 79.99,
        'expense_date': '2025-08-12',
    }, headers=auth_headers)

    client.post('/api/expenses', json={
        'name': 'In n out',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-05-25',
    }, headers=auth_headers)

    response = client.get('/api/expenses', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['expenses']) == 3
    assert data['pagination']['total'] == 3

def test_get_expenses_by_category(client, auth_headers):
    client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-02-06',
    }, headers=auth_headers)

    client.post('/api/expenses', json={
        'name': 'Monitor',
        'category': 'Personal',
        'amount': 79.99,
        'expense_date': '2025-08-12',
    }, headers=auth_headers)

    client.post('/api/expenses', json={
        'name': 'In n out',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-05-25',
    }, headers=auth_headers)

    response = client.get('/api/expenses?category=Food', headers=auth_headers)

    assert response.status_code == 200
    data = response.get_json()
    expenses = data['expenses']
    
    assert all(e['category'] == 'Food' for e in expenses)
    assert len(expenses) == 2
    names = [e['name'] for e in expenses]

    assert 'Pho' in names
    assert 'In n out' in names
    assert 'Monitor' not in names

def test_get_expenses_by_date(client, auth_headers):
    client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-02-06',
    }, headers=auth_headers)

    client.post('/api/expenses', json={
        'name': 'Monitor',
        'category': 'Personal',
        'amount': 79.99,
        'expense_date': '2025-08-12',
    }, headers=auth_headers)

    client.post('/api/expenses', json={
        'name': 'In n out',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-05-25',
    }, headers=auth_headers)

    client.post('/api/expenses', json={
        'name': 'Gas',
        'category': 'Transit',
        'amount': 42.8,
        'expense_date': '2025-03-29',
    }, headers=auth_headers)

    response = client.get('/api/expenses?start_date=2025-01-01&end_date=2025-05-01', headers=auth_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert len(data['expenses']) == 2

    names = [e['name'] for e in data['expenses']]
    assert 'Pho' in names
    assert 'Gas' in names

