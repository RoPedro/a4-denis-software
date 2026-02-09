def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    
def test_valid_input(client):
    response = client.post('/api/v1/insert', data = {
        "title": "Duh",
        "author": "Foo Bar",
        "num_copies": 999 
    })
    assert response.status_code == 200