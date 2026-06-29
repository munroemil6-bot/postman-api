import sys
import os
import json
import pytest

# Ensure the root project directory is on the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import app

@pytest.fixture
def client():
    return app.test_client()

def test_homepage_returns_welcome_message(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "message" in data
    assert "welcome" in data["message"].lower()

def test_get_events_returns_event_list(client):
    response = client.get("/events")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all("id" in event and "title" in event for event in data)

def test_post_events_adds_new_event(client):
    payload = {"title": "New Test Event"}
    response = client.post("/events", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 201
    data = response.get_json()
    assert isinstance(data, dict)
    assert data["title"] == payload["title"]
    assert "id" in data

def test_post_event_missing_data_returns_error(client):
    response = client.post("/events", data=json.dumps({}), content_type="application/json")
    assert response.status_code == 400 or response.status_code == 422  # depending on your validation


def test_unknown_route_returns_not_found(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
