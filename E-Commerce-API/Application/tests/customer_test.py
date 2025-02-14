
CUSTOMER_BASE = "/customers"
CUSTOMER_ID = 1
CUSTOMER_URL = f"{CUSTOMER_BASE}/{CUSTOMER_ID}"

def test_create_customer(client):
    response = client.post(CUSTOMER_BASE, json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"

def test_get_customer(client):
    client.post(CUSTOMER_BASE, json={"name": "Alice", "email": "alice@example.com"})
    response = client.get(CUSTOMER_URL)
    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"

def test_update_customer(client):
    client.post(CUSTOMER_BASE, json={"name": "Bob", "email": "bob@example.com"})
    response = client.put(CUSTOMER_URL, json={"name": "Bobby"})
    assert response.status_code == 200
    assert response.json()["name"] == "Bobby"

def test_delete_customer(client):
    client.post(CUSTOMER_BASE, json={"name": "Eve", "email": "eve@example.com"})
    response = client.delete(CUSTOMER_URL)
    assert response.status_code == 200 
