from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: No setup necesario

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert f"Signed up {email} for {activity}" in data["message"]

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_unregister_participant():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"{email} has been removed from {activity}" in response.json()["message"]
