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
        {"name": "vodka"},
        {"name": "lime juice"},
        {"name": "triple sec"}
    ])
    response = client.get("/api/suggestions/available")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
