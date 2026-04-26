
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def get_auth_token():
    # Try to register, fallback to login if user exists
    reg_resp = client.post("/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    if reg_resp.status_code == 200:
        return reg_resp.json()["access_token"]
    login_resp = client.post("/login", data={
        "username": "testuser@example.com",
        "password": "testpass123"
    })
    assert login_resp.status_code == 200
    return login_resp.json()["access_token"]

def test_create_calculation():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    # Create calculation
    response = client.post("/api/calculations", json={
        "a": 10,
        "b": 5,
        "type": "Add"
    }, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["a"] == 10
    assert data["b"] == 5
    assert data["type"] == "Add"
    assert data["result"] == 15
    calc_id = data["id"]

    # Read calculation
    get_resp = client.get(f"/api/calculations/{calc_id}", headers=headers)
    assert get_resp.status_code == 200
    get_data = get_resp.json()
    assert get_data["id"] == calc_id
    assert get_data["result"] == 15

    # Edit calculation
    put_resp = client.put(f"/api/calculations/{calc_id}", json={
        "a": 20,
        "b": 2,
        "type": "Multiply"
    }, headers=headers)
    assert put_resp.status_code == 200
    put_data = put_resp.json()
    assert put_data["result"] == 40

    # Browse calculations
    browse_resp = client.get("/api/calculations", headers=headers)
    assert browse_resp.status_code == 200
    assert any(c["id"] == calc_id for c in browse_resp.json())

    # Delete calculation
    del_resp = client.delete(f"/api/calculations/{calc_id}", headers=headers)
    assert del_resp.status_code == 200
    assert del_resp.json()["detail"] == "Calculation deleted"

    # Confirm deletion
    get_resp2 = client.get(f"/api/calculations/{calc_id}", headers=headers)
    assert get_resp2.status_code == 404

def test_invalid_calculation_type():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/calculations", json={
        "a": 1,
        "b": 2,
        "type": "Modulo"
    }, headers=headers)
    assert response.status_code == 422

def test_divide_by_zero():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/calculations", json={
        "a": 5,
        "b": 0,
        "type": "Divide"
    }, headers=headers)
    assert response.status_code == 422
    assert any("Division by zero" in err["msg"] for err in response.json()["detail"])
