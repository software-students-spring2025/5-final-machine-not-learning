import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.db import get_favorites_collection
from datetime import datetime
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_add_favorite(client):
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
    db = get_favorites_collection()
    db.delete_many({})
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
    assert any("gin fizz" in item["info"] for item in data)
    
def test_delete_favorite_success(client):
    db = get_favorites_collection()
    db.delete_many({})
    db.insert_one({
        "name": "negroni",
        "ingredients": ["gin", "vermouth", "campari"],
        "instructions": "Stir all ingredients with ice, then strain into glass.",
        "user_id": "test-user",
        "added_on": datetime.utcnow().isoformat()
    })

    response = client.delete("/api/favorites/negroni")
    assert response.status_code == 200


def test_delete_favorite_not_found(client):
    db = get_favorites_collection()
    db.delete_many({})
    response = client.delete("/api/favorites/does-not-exist")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Item not found"
