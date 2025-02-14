import pytest
from bson import ObjectId
from datetime import datetime


def test_create_blog(client, mock_db, sample_blog):
    mock_db.insert_one.return_value.inserted_id = sample_blog["_id"]

    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2FkOTgyYjU3ZTA3NDk1NWY5NjY3NjMiLCJleHAiOjE3Mzk0MzA5Nzd9.jevn4eg5bDQMJ3tsht7yRwjHhLqttAprosUhOy-ErMU"
    }

    response = client.post("/blogs/create", json={
        "title": "Test Blog",
        "content": "This is a test blog",
        "author": "Akshita",
    }, headers=headers)

    assert response.status_code == 201


def test_read_blogs(client, mock_db, sample_blog):
    mock_db.find.return_value.skip.return_value.limit.return_value = [sample_blog]
    mock_db.count_documents.return_value = 1

    response = client.get("/blogs?page=1&page_size=2")

    assert response.status_code == 200


   