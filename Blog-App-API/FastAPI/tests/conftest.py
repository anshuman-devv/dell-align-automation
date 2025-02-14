import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from bson import ObjectId
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from index import app

# from Application.config.db import get_collection  # Ensure correct import


@pytest.fixture(scope="module")
def client():   
    return TestClient(app)


@pytest.fixture
def mock_db():
    with patch("Application.config.db.get_collection") as mock_get_collection:
        mock_collection = MagicMock()
        mock_get_collection.return_value = mock_collection
        yield mock_collection



@pytest.fixture
def mock_auth(mocker):
    mocker.patch("Application.auth.get_current_user", return_value={"user_id": "test_user"})


@pytest.fixture
def sample_blog():
    return  {             
    "_id": ObjectId(), 
    "title": "Test Blog",
    "content": "This is a test blog",
    "author": "Akshita",
    "creation": datetime.utcnow().timestamp()
    }


@pytest.fixture
def sample_comment(sample_blog):
    return {
        "_id": ObjectId('67ad9432b1e4faf6b8743acf'),
        "text": "This is a test comment",
        "blog_id": sample_blog["_id"],
        "author": "Anshuman",
        "created_at": 1707763200
    }


@pytest.fixture
def sample_user():
    return {
    "_id": ObjectId(),
    "username": "Akshita",
    "email": "akshita@gmail.com",
    "hashed_password": "password123"
    }