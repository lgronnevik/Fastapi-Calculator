import pytest
import uuid
from playwright.async_api import async_playwright
import pytest_asyncio

BASE_URL = "http://localhost:8000"

@pytest_asyncio.fixture(scope="session")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()

@pytest_asyncio.fixture(scope="function")
async def page(browser):
    page = await browser.new_page()
    yield page
    await page.close()

@pytest.mark.asyncio
async def test_register_success(page):
    await page.goto(f"{BASE_URL}/register")
    unique = str(uuid.uuid4())[:8]
    email = f"test_{unique}@example.com"
    await page.fill('input[type="email"]', email)
    await page.fill('input#password', "password123")
    await page.fill('input#confirm', "password123")
    await page.click('button[type="submit"]')
    await page.wait_for_selector('.success')
    assert "Registration successful" in await page.inner_text('#message')

@pytest.mark.asyncio
async def test_register_short_password(page):
    await page.goto(f"{BASE_URL}/register")
    await page.fill('input[type="email"]', "shortpass@example.com")
    await page.fill('input#password', "123")
    await page.fill('input#confirm', "123")
    await page.click('button[type="submit"]')
    await page.wait_for_function(
        "() => document.getElementById('message').textContent.includes('Password must be at least 6 characters.')"
    )
    assert "Password must be at least 6 characters" in await page.inner_text('#message')

@pytest.mark.asyncio
async def test_login_success(page):
    # Register first
    unique = str(uuid.uuid4())[:8]
    email = f"login_{unique}@example.com"
    password = "password123"
    await page.goto(f"{BASE_URL}/register")
    await page.fill('input[type="email"]', email)
    await page.fill('input#password', password)
    await page.fill('input#confirm', password)
    await page.click('button[type="submit"]')
    await page.wait_for_selector('.success')
    # Now login
    await page.goto(f"{BASE_URL}/login")
    await page.fill('input[type="email"]', email)
    await page.fill('input#password', password)
    await page.click('button[type="submit"]')
    await page.wait_for_selector('.success')
    assert "Login successful" in await page.inner_text('#message')

@pytest.mark.asyncio
async def test_login_wrong_password(page):
    # Register first
    unique = str(uuid.uuid4())[:8]
    email = f"wrongpass_{unique}@example.com"
    password = "password123"
    await page.goto(f"{BASE_URL}/register")
    await page.fill('input[type="email"]', email)
    await page.fill('input#password', password)
    await page.fill('input#confirm', password)
    await page.click('button[type="submit"]')
    await page.wait_for_selector('.success')
    # Now login with wrong password
    await page.goto(f"{BASE_URL}/login")
    await page.fill('input[type="email"]', email)
    await page.fill('input#password', "wrongpassword")
    await page.click('button[type="submit"]')
    await page.wait_for_selector('.error')
    assert "Invalid email or password" in await page.inner_text('#message')
