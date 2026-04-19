
import sys
import asyncio
import uuid
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_server_reachable(page):
    response = await page.goto(f"{BASE_URL}/")
    print("\n\n--- Server reachability test ---\n")
    print("Status:", response.status if response else "No response")
    print("\n--- end server reachability test ---\n")
    assert response is not None and response.status == 200

# ...existing code...

@pytest.mark.asyncio
async def test_debug_register_page(page):

    await page.goto(f"{BASE_URL}/register")
    content = await page.content()
    print("\n\n--- /register page content ---\n")
    print(content)
    print("\n--- end /register page content ---\n")

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
    print('Navigating to /register')
    await page.goto(f"{BASE_URL}/register")
    print('Filling email')
    unique = str(uuid.uuid4())[:8]
    email = f"test_{unique}@example.com"
    await page.fill('input[type="email"]', email)
    print('Filling password')
    await page.fill('input#password', "password123")
    await page.fill('input#confirm', "password123")
    print('Clicking submit')
    await page.click('button[type="submit"]')
    print('Waiting for .success selector')
    await page.wait_for_selector('.success', timeout=5000)
    print('Checking message')
    assert "Registration successful" in await page.inner_text('#message')

@pytest.mark.asyncio
async def test_register_short_password(page):
    await page.goto(f"{BASE_URL}/register")
    await page.fill('input[type="email"]', "shortpass@example.com")
    await page.fill('input#password', "123")
    await page.fill('input#confirm', "123")
    await page.click('button[type="submit"]')
    await page.wait_for_function(
        "() => document.getElementById('message').textContent.includes('Password must be at least 6 characters.')",
        timeout=5000
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
    await page.wait_for_selector('.success', timeout=5000)
    # Now login
    await page.goto(f"{BASE_URL}/login")
    await page.fill('input[type="email"]', email)
    await page.fill('input#password', password)
    await page.click('button[type="submit"]')
    await page.wait_for_selector('.success', timeout=5000)
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
    await page.wait_for_selector('.success', timeout=5000)
    # Now login with wrong password
    await page.goto(f"{BASE_URL}/login")
    await page.fill('input[type="email"]', email)
    await page.fill('input#password', "wrongpassword")
    await page.click('button[type="submit"]')
    await page.wait_for_selector('.error', timeout=5000)
    assert "Invalid email or password" in await page.inner_text('#message')
