from app.auth import hash_password, verify_password

def test_hash_password():
    password = "test123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)