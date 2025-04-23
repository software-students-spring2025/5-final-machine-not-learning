import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.db import get_inventory_collection

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_suggestions(client):
    db = get_inventory_collection()
    db.delete_many({})
    db.insert_many([
        {"name": "vodka", "user_id": "test-user"},
        {"name": "lime juice", "user_id": "test-user"},
        {"name": "triple sec", "user_id": "test-user"}
    ])

    response = client.get("/api/suggestions/available")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, dict)
    assert "matched" in data
    assert isinstance(data["matched"], list)
