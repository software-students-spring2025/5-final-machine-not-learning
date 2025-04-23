import pytest
from flask import json
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("openai.ChatCompletion.create")
def test_ai_response(mock_create, client):
    mock_create.return_value = {
        "choices": [{"message": {"content": "Try a Mojito"}}]
    }

    response = client.post("/api/ai/ask", json={"prompt": "What can I make with rum and mint?"})
    assert response.status_code == 200
    assert "Mojito" in response.get_json().get("recommendation", "")
