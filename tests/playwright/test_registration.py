import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
import uuid

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
async def test_registration_page_loads(page):
    await page.goto(f"{BASE_URL}/auth/register")
    assert await page.title() == "Register"
    assert await page.locator("h3, h2", has_text="Register").is_visible()
    assert await page.locator("input[name='username']").is_visible()
    assert await page.locator("input[name='email']").is_visible()
    assert await page.locator("input[name='password']").is_visible()

@pytest.mark.asyncio
async def test_register_new_user(page):
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    await page.goto(f"{BASE_URL}/auth/register")
    await page.fill("input[name='username']", username)
    await page.fill("input[name='email']", f"{username}@example.com")
    await page.fill("input[name='password']", "testpass123")
    await page.select_option("select[name='role']", "coder")
    await page.click("button[type='submit']")
    await page.wait_for_url(f"{BASE_URL}/auth/login")
    content = await page.content()
    assert "Registration successful" in content or "login" in content.lower() 