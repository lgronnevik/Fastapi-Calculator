from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_user():
    unique_id = str(uuid.uuid4())[:8]
    username = f"testuser_{unique_id}"
    email = f"test_{unique_id}@example.com"

    response = client.post("/register", json={
        "username": username,
        "email": email,
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.json()
    # Only access_token and token_type are returned
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Test login with the same credentials
    login_response = client.post(
        "/login",
        data={"username": email, "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"