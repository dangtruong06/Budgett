# test delete expense - DELETE
def test_delete_expense_not_found(client, auth_headers):
    response = client.delete('/api/expenses/9999', headers=auth_headers)
    
    assert response.status_code == 404

def test_delete_expense(client, auth_headers):
    create_response = client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-08-12',
    }, headers=auth_headers)
    expense_id = create_response.get_json()['id']

    response = client.delete(f'/api/expenses/{expense_id}',
                             headers=auth_headers)

    assert response.status_code == 204

    get_response = client.get(f'/api/expense/{expense_id}', headers=auth_headers)
    assert get_response.status_code == 404

def test_delete_expense_wrong_user(client, auth_headers, other_auth_headers):
    create_response = client.post('/api/expenses', json={
        'name': 'Pho',
        'category': 'Food',
        'amount': 30.4,
        'expense_date': '2025-08-12',
    }, headers=auth_headers)
    expense_id = create_response.get_json()['id']

    response = client.delete(f'/api/expenses/{expense_id}', 
                             headers=other_auth_headers)
    
    assert response.get_json() == {'error': 'unauthorized'}
    assert response.status_code == 403




