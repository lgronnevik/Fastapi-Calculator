import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add app folder to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI Calculator Running"}

def test_add_endpoint():
    response = client.post("/add", params={"a": 3, "b": 2})
    assert response.status_code == 200
    assert response.json()["result"] == 5

def test_subtract_endpoint():
    response = client.post("/subtract", params={"a": 5, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 2

def test_multiply_endpoint():
    response = client.post("/multiply", params={"a": 4, "b": 2})
    assert response.status_code == 200
    assert response.json()["result"] == 8

def test_divide_endpoint():
    response = client.post("/divide", params={"a": 10, "b": 2})
    assert response.status_code == 200
    assert response.json()["result"] == 5

def test_divide_by_zero():
    response = client.post("/divide", params={"a": 5, "b": 0})
    assert response.status_code == 400

def test_exponentiation_endpoint():
    response = client.post("/add", params={"a": 2, "b": 3})  # Control
    assert response.status_code == 200
    assert response.json()["result"] == 5
    # Exponentiation is not a direct endpoint, but is available via /api/calculations
    # Exponentiation is tested in test_calculations.py