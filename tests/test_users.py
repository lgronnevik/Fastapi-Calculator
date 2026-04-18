from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_user():
    unique_id = str(uuid.uuid4())[:8]
    username = f"testuser_{unique_id}"
    email = f"test_{unique_id}@example.com"

    response = client.post("/users/register", json={
        "username": username,
        "email": email,
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert data["email"] == email

    # Test login with the same credentials
    login_response = client.post(
        "/users/login",
        data={"username": username, "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert login_data["username"] == username
    assert login_data["email"] == email