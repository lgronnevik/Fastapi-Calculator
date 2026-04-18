import pytest
from playwright.sync_api import sync_playwright
import uuid

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def test_register_success(page):
    page.goto(f"{BASE_URL}/register")
    unique = str(uuid.uuid4())[:8]
    email = f"test_{unique}@example.com"
    page.fill('input[type="email"]', email)
    page.fill('input#password', "password123")
    page.fill('input#confirm', "password123")
    page.click('button[type="submit"]')
    page.wait_for_selector('.success')
    assert "Registration successful" in page.inner_text('#message')

def test_register_short_password(page):
    page.goto(f"{BASE_URL}/register")
    page.fill('input[type="email"]', "shortpass@example.com")
    page.fill('input#password', "123")
    page.fill('input#confirm', "123")
    page.click('button[type="submit"]')
    page.wait_for_function(
        """() => document.getElementById('message').textContent.includes('Password must be at least 6 characters.')"""
    )
    assert "Password must be at least 6 characters" in page.inner_text('#message')

def test_login_success(page):
    # Register first
    unique = str(uuid.uuid4())[:8]
    email = f"login_{unique}@example.com"
    password = "password123"
    page.goto(f"{BASE_URL}/register")
    page.fill('input[type="email"]', email)
    page.fill('input#password', password)
    page.fill('input#confirm', password)
    page.click('button[type="submit"]')
    page.wait_for_selector('.success')
    # Now login
    page.goto(f"{BASE_URL}/login")
    page.fill('input[type="email"]', email)
    page.fill('input#password', password)
    page.click('button[type="submit"]')
    page.wait_for_selector('.success')
    assert "Login successful" in page.inner_text('#message')

def test_login_wrong_password(page):
    # Register first
    unique = str(uuid.uuid4())[:8]
    email = f"wrongpass_{unique}@example.com"
    page.goto(f"{BASE_URL}/register")
    page.fill('input[type="email"]', email)
    page.fill('input#password', "password123")
    page.fill('input#confirm', "password123")
    page.click('button[type="submit"]')
    page.wait_for_selector('.success')
    # Now login with wrong password
    page.goto(f"{BASE_URL}/login")
    page.fill('input[type="email"]', email)
    page.fill('input#password', "wrongpassword")
    page.click('button[type="submit"]')
    page.wait_for_selector('.error')
    assert "Login failed" in page.inner_text('#message') or "Invalid" in page.inner_text('#message')
