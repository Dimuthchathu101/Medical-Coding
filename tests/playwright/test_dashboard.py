import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

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
    # Login as admin
    await page.goto(f"{BASE_URL}/auth/login")
    await page.fill("input[name='username']", "admin")
    await page.fill("input[name='password']", "admin123")
    await page.click("button[type='submit']")
    await page.wait_for_url(f"{BASE_URL}/patients/")
    yield page
    await context.close()

@pytest.mark.asyncio
async def test_dashboard_access(page):
    await page.goto(f"{BASE_URL}/billing/dashboard")
    content = await page.content()
    assert "Billing & Claims Dashboard" in content or "Dashboard" in await page.title()
    assert "Total Claims" in content
    assert "Upcoming Appointments" in content 