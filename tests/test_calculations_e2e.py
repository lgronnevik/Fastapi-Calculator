import sys
import asyncio
import random
from playwright.async_api import async_playwright

# Utility to generate a random email for registration
def random_email():
    return f"testuser{random.randint(10000,99999)}@example.com"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        base_url = "http://localhost:8000"

        # Register a new user
        await page.goto(f"{base_url}/register")
        email = random_email()
        await page.fill('input[name="username"]', "testuser")
        await page.fill('input[name="email"]', email)
        await page.fill('input[name="password"]', "testpass123")
        await page.click('button[type="submit"]')
        # Wait for redirect or token
        await page.wait_for_timeout(1000)

        # Go to calculations page
        await page.goto(f"{base_url}/calculations")
        assert "My Calculations" in await page.content()

        # Add a calculation
        await page.click('a[href="/calculations/add"]')
        await page.fill('input[name="a"]', "10")
        await page.fill('input[name="b"]', "5")
        await page.select_option('select[name="type"]', "Add")
        await page.click('button[type="submit"]')
        await page.wait_for_url(f"{base_url}/calculations")
        assert "10" in await page.content()
        assert "5" in await page.content()
        assert "Add" in await page.content()

        # Read calculation details
        await page.click('a:has-text("Read")')
        assert "Calculation Details" in await page.content()
        await page.go_back()

        # Edit calculation
        await page.click('a:has-text("Edit")')
        await page.fill('input[name="a"]', "20")
        await page.click('button[type="submit"]')
        await page.wait_for_url(f"{base_url}/calculations/")
        assert "20" in await page.content()

        # Delete calculation
        await page.goto(f"{base_url}/calculations")
        await page.click('button:has-text("Delete")')
        await page.wait_for_url(f"{base_url}/calculations")
        # Calculation should be gone
        assert "20" not in await page.content()

        # Negative: Division by zero
        await page.click('a[href="/calculations/add"]')
        await page.fill('input[name="a"]', "10")
        await page.fill('input[name="b"]', "0")
        await page.select_option('select[name="type"]', "Divide")
        await page.click('button[type="submit"]')
        assert "Division by zero is not allowed" in await page.content()

        await browser.close()

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run())
