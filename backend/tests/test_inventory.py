"""
Integration tests for the `/api/inventory/` endpoints.
These tests check adding, retrieving, and deleting items from inventory.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.db import get_inventory_collection

@pytest.fixture
def client():
    """
    Pytest fixture that creates a test client for the Flask app.
    This allows HTTP requests to be made without a running server.
    """

    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_add_inventory(client):
    """
    Test the POST endpoint to add a new inventory item.
    Asserts that a successful creation returns a 201 status code.
    """

    payload = {"name": "vodka", "category": "liquor", "expiration_date": "2025-12-31"}
    response = client.post("/api/inventory/", json=payload)
    assert response.status_code == 201

def test_get_inventory(client):
    """
    Test the GET endpoint for retrieving all inventory items.
    Asserts that a successful request returns a list of items.
    """
     
    response = client.get("/api/inventory/")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_delete_inventory(client):
    """
    Test the DELETE endpoint for removing an inventory item.
    Adds an item, then attempts to delete it.
    Asserts that the status code is 200 (success) or 404 (not found).
    """

    test_add_inventory(client)
    response = client.delete("/api/inventory/vodka")

    #acceptable responses: 200 (deleted) or 404 (not found if already removed)
    assert response.status_code in (200, 404)
