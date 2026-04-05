from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"