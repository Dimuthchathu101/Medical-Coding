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
    # Login as admin
    await page.goto(f"{BASE_URL}/auth/login")
    await page.fill("input[name='username']", "admin")
    await page.fill("input[name='password']", "admin123")
    await page.click("button[type='submit']")
    await page.wait_for_url(f"{BASE_URL}/patients/")
    yield page
    await context.close()

@pytest.mark.asyncio
async def test_add_patient(page):
    await page.goto(f"{BASE_URL}/patients/add")
    await page.fill("input[name='first_name']", "Test")
    await page.fill("input[name='last_name']", f"Patient{uuid.uuid4().hex[:6]}")
    await page.fill("input[name='dob']", "1990-01-01")
    await page.fill("input[name='insurance']", "Test Insurance")
    await page.click("button[type='submit']")
    content = await page.content()
    assert "Patient added successfully" in content

@pytest.mark.asyncio
async def test_patient_list_and_view(page):
    await page.goto(f"{BASE_URL}/patients/")
    assert "My Patients" in await page.content()
    # Click the first patient link
    first_link = page.locator("table a").first
    await first_link.click()
    assert "Patient Details" in await page.content() 