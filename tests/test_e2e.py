import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"

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

def test_home_page(page):
    page.goto(BASE_URL)
    assert "FastAPI Calculator Running" in page.content()

def test_add_numbers(page):
    page.goto(f"{BASE_URL}/docs")
    page.click('text=/add')
    page.click('text="Try it out"')
    page.fill('input[placeholder="a"]', "3")
    page.fill('input[placeholder="b"]', "2")
    page.click('text="Execute"')
    output = page.locator("text=5")
    assert output.count() > 0

def test_divide_by_zero(page):
    page.goto(f"{BASE_URL}/docs")
    page.click('text=/divide')
    page.click('text="Try it out"')
    page.fill('input[placeholder="a"]', "5")
    page.fill('input[placeholder="b"]', "0")
    page.click('text="Execute"')
    output = page.locator("text=Cannot divide by zero")
    assert output.count() > 0