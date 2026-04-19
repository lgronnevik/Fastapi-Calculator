import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_minimal_server_reachable():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = await browser.new_page()
        print("[DEBUG] Navigating to / ...")
        response = await page.goto(f"{BASE_URL}/")
        print("[DEBUG] Navigation complete.")
        assert response is not None and response.status == 200
        await browser.close()
