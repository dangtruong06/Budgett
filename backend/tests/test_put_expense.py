# test update expenses - PUT   
def test_update_expense(client, auth_headers):
    # make expense
    create_response = client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-08-12',
    }, headers=auth_headers)
    expense_id = create_response.get_json()['id']

    # update expense
    response = client.put(f'/api/expenses/{expense_id}', json={
        'amount': 35.43
    }, headers=auth_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['amount'] == 35.43
    assert data['name'] == 'Pho'
    assert data['category'] == 'Food'
    assert data['expense_date'] == '2025-08-12'

def test_update_expense_not_found(client, auth_headers):
    response = client.put('/api/expenses/99999', json={
        'name': 'Everyday Sushi'
    },
    headers=auth_headers)

    assert response.status_code == 404

def test_update_expense_wrong_user(client, auth_headers, other_auth_headers):
    create_response = client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-08-12',
    }, headers=auth_headers)
    expense_id = create_response.get_json()['id']

    response = client.put(f'/api/expenses/{expense_id}', json={
        'name': 'Pho Good'
    }, headers=other_auth_headers)

    assert response.status_code == 403
    assert response.get_json() == {'error': 'unauthorized'}