import pytest
from bson import ObjectId

def test_create_comment(client, mock_db, sample_blog, sample_comment):
    mock_db.insert_one.return_value.inserted_id = sample_comment["_id"]

    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2FkOTgyYjU3ZTA3NDk1NWY5NjY3NjMiLCJleHAiOjE3Mzk0MzA5Nzd9.jevn4eg5bDQMJ3tsht7yRwjHhLqttAprosUhOy-ErMU"
    }

    response = client.post(f"/comments/blog/{sample_blog['_id']}/create", json={
        "blog_id": str(sample_blog["_id"]),
        "author": "Anshuman",
        "text": "This is a test comment"
    }, headers=headers)

    assert response.status_code == 201


def test_read_comment_success(client, mock_db, sample_comment):
    mock_db.find_one.return_value = {**sample_comment, "_id": str(sample_comment["_id"])}
    print(f"Mocked Comment ID: {str(sample_comment['_id'])}")

    response = client.get(f"/comments/{str(sample_comment['_id'])}")    
    print(f"Response Status: {response.status_code}, Response Body: {response.json()}")

    assert response.status_code == 200


def test_read_comment_not_found(client, mock_db):
    mock_db.find_one.return_value = None
    random_id = str(ObjectId())

    response = client.get(f"/comments/{random_id}")
    print(f"Response Status: {response.status_code}, Response Body: {response.json()}")

    assert response.status_code == 404


