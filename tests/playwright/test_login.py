import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
import asyncio

BASE_URL = "http://127.0.0.1:5000"

@pytest_asyncio.fixture(scope="session")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()

@pytest_asyncio.fixture
async def page(browser):
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await context.close()

@pytest.mark.asyncio
async def test_login_page_loads(page):
    await page.goto(f"{BASE_URL}/auth/login")
    assert await page.title() == "Login"
    assert await page.locator("h3", has_text="Login").is_visible()
    assert await page.locator("button[type='submit']").is_visible()
    assert await page.locator("input[name='username']").is_visible()
    assert await page.locator("input[name='password']").is_visible()

@pytest.mark.asyncio
async def test_login_valid_credentials(page):
    await page.goto(f"{BASE_URL}/auth/login")
    await page.fill("input[name='username']", "admin")
    await page.fill("input[name='password']", "admin123")
    await page.click("button[type='submit']")
    await page.wait_for_url(f"{BASE_URL}/patients/")
    content = await page.content()
    assert "Patients" in content or "Dashboard" in content 