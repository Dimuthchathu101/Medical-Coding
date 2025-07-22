import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
import uuid
from datetime import datetime, timedelta

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
async def test_schedule_edit_cancel_appointment(page):
    patient_id = await get_first_patient_id(page)
    await page.goto(f"{BASE_URL}/patients/{patient_id}/appointments/add")
    dt = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
    await page.fill("input[name='date_time']", dt)
    await page.fill("input[name='reason']", "Routine Checkup")
    await page.click("button[type='submit']")
    content = await page.content()
    assert "Appointment scheduled successfully" in content
    # Edit appointment
    await page.goto(f"{BASE_URL}/patients/{patient_id}/appointments")
    edit_link = page.locator("a.btn-warning").first
    await edit_link.click()
    await page.fill("input[name='reason']", "Updated Reason")
    await page.click("button[type='submit']")
    content = await page.content()
    assert "Appointment updated successfully" in content
    # Cancel appointment
    await page.goto(f"{BASE_URL}/patients/{patient_id}/appointments")
    cancel_btn = page.locator("form button.btn-danger").first
    await cancel_btn.click()
    content = await page.content()
    assert "Appointment cancelled" in content 