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

def test_add_inventory(client):
    payload = {"name": "vodka", "category": "liquor", "expiration_date": "2025-12-31"}
    response = client.post("/api/inventory/", json=payload)
    assert response.status_code == 201

def test_get_inventory(client):
    response = client.get("/api/inventory/")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_delete_inventory(client):
    test_add_inventory(client)
    response = client.delete("/api/inventory/vodka")
    assert response.status_code in (200, 404)
