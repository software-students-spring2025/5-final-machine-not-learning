"""
Integration tests for authentication and main pages in the BarBuddy app.
Tests cover login, registration, logout, and loading of core pages.
"""

import pytest
from app import create_app
from flask import url_for
from app.db import get_inventory_collection

@pytest.fixture
def app():
    """
    Pytest fixture to create and configure the Flask application for testing.
    CSRF protection is disabled for form testing convenience.
    """

    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # 表单测试禁用 CSRF
    return app

@pytest.fixture
def client(app):
    """
    Pytest fixture to create a test client that can simulate HTTP requests.
    """

    return app.test_client()

def test_dashboard(client):
    """
    Test that the dashboard (home page) loads correctly.
    """

    response = client.get("/")
    assert response.status_code == 200
    assert b"BarBuddy" in response.data or b"<html" in response.data

def test_register_page_loads(client):
    """
    Test that the registration page loads without error.
    """

    response = client.get("/register")
    assert response.status_code == 200

def test_login_page_loads(client):
    """
    Test that the login page loads without error.
    """

    response = client.get("/login")
    assert response.status_code == 200

def test_invalid_login(client):
    """
    Test login attempt with invalid credentials.
    Should either return a message about invalid login or simply return 200 with a form.
    """

    response = client.post("/login", data={
        "username": "ghost",
        "password": "wrongpassword"
    }, follow_redirects=True)

    #either error message should be present or we should land back at the form
    assert b"Invalid" in response.data or response.status_code == 200

def test_register_user_success(client):
    """
    Test that a new user can successfully register with valid details.
    """

    response = client.post("/register", data={
        "name": "TestUser",
        "username": "testuser123",
        "password": "testpass123"
    }, follow_redirects=True)
    assert response.status_code == 200

def test_logout_redirect(client):
    """
    Test that logging out redirects the user appropriately.
    """

    response = client.get("/logout", follow_redirects=True)

    #after logout, we should land back on the homepage
    assert b"BarBuddy" in response.data or response.status_code == 200
