import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
import uuid
from datetime import datetime

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

async def get_first_patient_id(page):
    await page.goto(f"{BASE_URL}/patients/")
    link = page.locator("table a").first
    href = await link.get_attribute("href")
    return href.split("/")[-1]

@pytest.mark.asyncio
async def test_add_edit_claim_and_invoice(page):
    patient_id = await get_first_patient_id(page)
    await page.goto(f"{BASE_URL}/claims/patient/{patient_id}/claims/add")
    await page.fill("input[name='amount']", "123.45")
    await page.select_option("select[name='status']", "pending")
    # Select at least one code if available
    await page.click("#icd10-codes")
    await page.keyboard.press("ArrowDown")
    await page.keyboard.press("Enter")
    await page.click("#cpt-codes")
    await page.keyboard.press("ArrowDown")
    await page.keyboard.press("Enter")
    await page.click("button[type='submit']")
    content = await page.content()
    assert "Claim created successfully" in content
    # Edit claim
    await page.goto(f"{BASE_URL}/claims/patient/{patient_id}/claims")
    edit_link = page.locator("a.btn-warning").first
    await edit_link.click()
    await page.fill("input[name='amount']", "200.00")
    await page.select_option("select[name='status']", "submitted")
    await page.click("button[type='submit']")
    content = await page.content()
    assert "Claim updated successfully" in content
    # Download invoice
    await page.goto(f"{BASE_URL}/claims/patient/{patient_id}/claims")
    invoice_link = page.locator("a.btn-outline-primary").first
    async with page.expect_download() as download_info:
        await invoice_link.click()
    download = await download_info.value
    assert download.suggested_filename.startswith("invoice_claim_") 