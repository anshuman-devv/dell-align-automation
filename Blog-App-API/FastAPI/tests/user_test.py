
def test_signup_success(client, mock_db, sample_user):
    mock_db.find_one.return_value = None
    mock_db.insert_one.return_value.inserted_id = sample_user["_id"]

    response = client.post("/auth/signup", json={
        "username": "Anshuman",
        "email": "anshuman@gmail.com",
        "password": "password123"
    })
    print(response.json())


    assert response.status_code == 200


def test_signup_existing_email(client, mock_db, sample_user):
    mock_db.find_one.return_value = sample_user

    response = client.post("/auth/signup", json={
        "username": "Anshuman",
        "email": "anshuman@gmail.com",
        "password": "password123"
    })

    assert response.status_code == 400


def test_login_success(client, mock_db, sample_user):
    mock_db.find_one.return_value = sample_user

    response = client.post("/auth/login", json={
        "email": "akshita@gmail.com",
        "password": "password123"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials(client, mock_db, sample_user):
    mock_db.find_one.return_value = sample_user

    response = client.post("/auth/login", json={
        "email": "akshita@gmail.com",
        "password": "password"
    })
    print(response.json())

    assert response.status_code == 401
