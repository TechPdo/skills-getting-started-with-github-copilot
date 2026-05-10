import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_get_activities(client):
    # Arrange: (client fixture sets up the app)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_duplicate(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Act (duplicate)
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

def test_signup_not_found(client):
    # Arrange
    email = "ghost@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister(client):
    # Arrange
    email = "removeuser@mergington.edu"
    activity = "Programming Class"
    # First, sign up
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]
    # Act (try again)
    response2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response2.status_code == 404
    assert "Participant not found" in response2.json()["detail"]
