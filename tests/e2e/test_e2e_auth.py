
# WINDOWS EVENT LOOP POLICY FIX: Must be first!
import sys
import asyncio
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import httpx
import uuid
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_server_reachable(page):
    print("[DEBUG] Navigating to / ...")
    response = await page.goto(f"{BASE_URL}/")
    print("[DEBUG] Navigation complete.")
    print("\n\n--- Server reachability test ---\n")
    print("Status:", response.status if response else "No response")
    print("\n--- end server reachability test ---\n")
    assert response is not None and response.status == 200

# ...existing code...

@pytest.mark.asyncio
async def test_debug_register_page(page):
    print("[DEBUG] Navigating to /register ...")
    await page.goto(f"{BASE_URL}/register")
    print("[DEBUG] Navigation complete.")
    content = await page.content()
    print("\n\n--- /register page content ---\n")
    print(content)
    print("\n--- end /register page content ---\n")

@pytest_asyncio.fixture(scope="session")
async def browser():
    print("\n[DEBUG] Launching Playwright browser (headless=True)...\n")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        print("[DEBUG] Playwright browser launched.")
        yield browser
        print("[DEBUG] Closing Playwright browser.")
        await browser.close()

@pytest_asyncio.fixture(scope="function")
async def page(browser):
    page = await browser.new_page()
    yield page
    await page.close()

@pytest.mark.asyncio
async def test_register_success(page):
    print('[DEBUG] Navigating to /register')
    await page.goto(f"{BASE_URL}/register")
    print('[DEBUG] Navigation complete.')
    print('[DEBUG] Filling email')
    unique = str(uuid.uuid4())[:8]
    email = f"test_{unique}@example.com"
    await page.fill('input[type="email"]', email)
    print('[DEBUG] Filling password')
    await page.fill('input#password', "password123")
    await page.fill('input#confirm', "password123")
    print('[DEBUG] Clicking submit')
    await page.click('button[type="submit"]')
    print('[DEBUG] Waiting for .success selector')
    await page.wait_for_selector('.success', timeout=5000)
    print('[DEBUG] Checking message')
    assert "Registration successful" in await page.inner_text('#message')

@pytest.mark.asyncio
async def test_register_short_password(page):
    print('[DEBUG] Navigating to /register')
    await page.goto(f"{BASE_URL}/register")
    print('[DEBUG] Navigation complete.')
    await page.fill('input[type="email"]', "shortpass@example.com")
    await page.fill('input#password', "123")
    await page.fill('input#confirm', "123")
    print('[DEBUG] Clicking submit')
    await page.click('button[type="submit"]')
    print('[DEBUG] Waiting for error message')
    await page.wait_for_function(
        "() => document.getElementById('message').textContent.includes('Password must be at least 6 characters.')",
        timeout=5000
    )
    print('[DEBUG] Checking message')
    assert "Password must be at least 6 characters" in await page.inner_text('#message')

@pytest.mark.asyncio
async def test_login_success(page):
    print('[DEBUG] Registering new user')
    unique = str(uuid.uuid4())[:8]
    email = f"login_{unique}@example.com"
    password = "password123"
    await page.goto(f"{BASE_URL}/register")
    print('[DEBUG] Registration page loaded')
    await page.fill('input[type="email"]', email)
    await page.fill('input#password', password)
    await page.fill('input#confirm', password)
    print('[DEBUG] Submitting registration')
    await page.click('button[type="submit"]')
    print('[DEBUG] Waiting for .success selector (register)')
    await page.wait_for_selector('.success', timeout=5000)
    print('[DEBUG] Registration success')
    print('[DEBUG] Navigating to /login')
    await page.goto(f"{BASE_URL}/login")
    print('[DEBUG] Login page loaded')
    await page.fill('input[type="email"]', email)
    await page.fill('input#password', password)
    print('[DEBUG] Submitting login')
    await page.click('button[type="submit"]')
    print('[DEBUG] Waiting for .success selector (login)')
    await page.wait_for_selector('.success', timeout=5000)
    print('[DEBUG] Login success')
    assert "Login successful" in await page.inner_text('#message')

@pytest.mark.asyncio
async def test_login_wrong_password(page):
    print('[DEBUG] Registering new user for wrong password test')
    unique = str(uuid.uuid4())[:8]
    email = f"wrongpass_{unique}@example.com"
    password = "password123"
    await page.goto(f"{BASE_URL}/register")
    print('[DEBUG] Registration page loaded')
    await page.fill('input[type="email"]', email)
    await page.fill('input#password', password)
    await page.fill('input#confirm', password)
    print('[DEBUG] Submitting registration')
    await page.click('button[type="submit"]')
    print('[DEBUG] Waiting for .success selector (register)')
    await page.wait_for_selector('.success', timeout=5000)
    print('[DEBUG] Registration success')
    print('[DEBUG] Navigating to /login')
    await page.goto(f"{BASE_URL}/login")
    print('[DEBUG] Login page loaded')
    await page.fill('input[type="email"]', email)
    await page.fill('input#password', "wrongpassword")
    print('[DEBUG] Submitting login')
    await page.click('button[type="submit"]')
    print('[DEBUG] Waiting for .error selector (login)')
    await page.wait_for_selector('.error', timeout=5000)
    print('[DEBUG] Login error shown')
    assert "Invalid email or password" in await page.inner_text('#message')
