import pytest
from datetime import datetime, timedelta
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

def test_expiring_alert(client):
    db = get_inventory_collection()
    db.delete_many({})
    soon = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    db.insert_one({
        "name": "lime juice",
        "expiration_date": soon,
        "user_id": "test-user"
    })

    response = client.get("/api/alerts/soon")
    assert response.status_code == 200

    data = response.get_json()
    combined = data.get("expired", []) + data.get("expiring_soon", [])

    assert any(item["name"] == "lime juice" for item in combined)
