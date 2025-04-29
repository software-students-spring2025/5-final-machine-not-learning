# tests/test_favorites.py

"""
Integration tests for the `/api/favorites/` endpoints.
Covers adding, retrieving, and deleting favorite cocktail recipes.
"""

import pytest
import sys
import os

#add project root to sys.path for imports to work in tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.db import get_favorites_collection
from datetime import datetime


@pytest.fixture
def client():
    """
    Fixture to provide a test client from the Flask app.
    Sets TESTING mode to True for isolated test behavior.
    """

    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_add_favorite(client):
    """
    Test adding a new favorite cocktail to the database.
    Asserts that the POST request returns a 201 and success message.
    """

    db = get_favorites_collection()
    db.delete_many({})
    payload = {
        "name": "vodka tonic",
        "ingredients": ["vodka", "tonic water"],
        "instructions": "Mix vodka and tonic water with ice and serve."
    }

    response = client.post("/api/favorites/", json=payload)
    assert response.status_code == 201
    assert response.get_json()["message"] == "Item added successfully"

def test_get_favorites(client):
    """
    Test retrieval of favorite cocktails from the database.
    Inserts one item and checks that it appears in the response.
    """

    db = get_favorites_collection()
    db.delete_many({})

    #insert a mock favorite item for testing
    db.insert_one({
        "info": "gin fizz",
        "category": "cocktail",
        "added_on": datetime.utcnow().isoformat(),
        "user_id": "test-user"
    })

    response = client.get("/api/favorites/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

    #ensure the inserted item is in the returned list
    assert any("gin fizz" in item["info"] for item in data)
    
def test_delete_favorite_success(client):
    """
    Test successful deletion of a favorite cocktail.
    Inserts and then deletes the same item.
    """

    db = get_favorites_collection()
    db.delete_many({})

    #add an item to be deleted
    db.insert_one({
        "name": "negroni",
        "ingredients": ["gin", "vermouth", "campari"],
        "instructions": "Stir all ingredients with ice, then strain into glass.",
        "user_id": "test-user",
        "added_on": datetime.utcnow().isoformat()
    })

    #attempt to delete the item via the API
    response = client.delete("/api/favorites/negroni")

    #check that deletion succeeded
    assert response.status_code == 200


def test_delete_favorite_not_found(client):
    """
    Test deletion of a non-existent favorite cocktail.
    Ensures the API returns 404 and proper error message.
    """

    db = get_favorites_collection()
    db.delete_many({})

    #attempt to delete a non-existent item
    response = client.delete("/api/favorites/does-not-exist")

    #expect a 404 Not Found response
    assert response.status_code == 404
    assert response.get_json()["error"] == "Item not found"
