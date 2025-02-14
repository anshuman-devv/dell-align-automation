ORDERS_BASE = "/orders"
CUSTOMER_BASE = "/customers"
PRODUCT_BASE = "/products"
ORDER_ID = 1
ORDER_URL = f"{ORDERS_BASE}/{ORDER_ID}"

def test_create_order(client):
    client.post(CUSTOMER_BASE, json={"name": "Sam", "email": "sam@example.com"})
    client.post(PRODUCT_BASE, json={"name": "Tablet", "description": "10-inch tablet", "price": 250.00})

    response = client.post("/orders", json={"customer_id": 1, "status": "PENDING"})
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"

def test_get_order(client):
    client.post(CUSTOMER_BASE, json={"name": "Lisa", "email": "lisa@example.com"})
    client.post(PRODUCT_BASE, json={"name": "Phone", "description": "Smartphone", "price": 500.00})
    client.post(ORDERS_BASE, json={"customer_id": 1, "status": "SHIPPED"})

    response = client.get(ORDER_URL)
    assert response.status_code == 200
    assert response.json()["status"] == "SHIPPED"

def test_update_order(client):
    client.post(CUSTOMER_BASE, json={"name": "Mike", "email": "mike@example.com"})
    client.post(PRODUCT_BASE, json={"name": "Headphones", "description": "Noise Cancelling", "price": 150.00})
    client.post(ORDERS_BASE, json={"customer_id": 1, "status": "PENDING"})

    response = client.put(ORDER_URL, json={"status": "DELIVERED"})
    assert response.status_code == 200
    assert response.json()["status"] == "DELIVERED"

def test_delete_order(client):
    client.post(CUSTOMER_BASE, json={"name": "Anna", "email": "anna@example.com"})
    client.post(PRODUCT_BASE, json={"name": "Camera", "description": "DSLR Camera", "price": 800.00})
    client.post(ORDERS_BASE, json={"customer_id": 1, "status": "PENDING"})

    response = client.delete(ORDER_URL)
    assert response.status_code == 200
