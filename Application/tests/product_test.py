PRODUCTS_BASE = "/products"
PRODUCT_ID = 1
PRODUCT_URL = f"{PRODUCTS_BASE}/{PRODUCT_ID}"

def test_create_product(client):
    response = client.post(PRODUCTS_BASE, json={"name": "Laptop", "description": "Gaming Laptop", "price": 1200.00})
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"

def test_get_product(client):
    client.post(PRODUCTS_BASE, json={"name": "Mouse", "description": "Wireless Mouse", "price": 20})
    response = client.get(PRODUCT_URL)
    assert response.status_code == 200
    assert response.json()["price"] == 20

def test_update_product(client):
    client.post("/products/", json={"name": "Keyboard", "description": "Mechanical Keyboard", "price": 100})
    response = client.put("/products/1", json={"name": "RGB Keyboard", "description": "Updated desc"})
    assert response.status_code == 200
    assert response.json()["name"] == "RGB Keyboard"

def test_delete_product(client):
    client.post(PRODUCTS_BASE, json={"name": "Monitor", "description": "4K Monitor", "price": 299})
    response = client.delete(PRODUCT_URL)
    assert response.status_code == 200