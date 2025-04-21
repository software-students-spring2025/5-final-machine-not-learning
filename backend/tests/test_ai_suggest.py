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

@patch("openai.OpenAI")
def test_ai_response(mock_openai, client):
    mock_chat = mock_openai.return_value.chat.completions.create
    mock_chat.return_value.choices = [
        type("obj", (object,), {"message": type("obj", (), {"content": "Test AI suggestion"})})
    ]

    response = client.post("/api/ai/ask", json={"prompt": "Surprise me"})
    assert response.status_code == 200
    assert "Test AI suggestion" in response.get_json()["recommendation"]
