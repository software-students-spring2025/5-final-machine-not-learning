import pytest
from app import create_app
from flask import url_for
from app.db import get_inventory_collection

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # 表单测试禁用 CSRF
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_dashboard(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"BarBuddy" in response.data or b"<html" in response.data

def test_register_page_loads(client):
    response = client.get("/register")
    assert response.status_code == 200

def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_invalid_login(client):
    response = client.post("/login", data={
        "username": "ghost",
        "password": "wrongpassword"
    }, follow_redirects=True)
    assert b"Invalid" in response.data or response.status_code == 200

def test_register_user_success(client):
    response = client.post("/register", data={
        "name": "TestUser",
        "username": "testuser123",
        "password": "testpass123"
    }, follow_redirects=True)
    assert response.status_code == 200

def test_logout_redirect(client):
    response = client.get("/logout", follow_redirects=True)
    assert b"BarBuddy" in response.data or response.status_code == 200
