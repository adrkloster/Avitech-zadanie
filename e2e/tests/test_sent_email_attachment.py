from dotenv import load_dotenv
import os
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import sync_playwright

load_dotenv()

scenarios('send_email_with_attachment.feature')

def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page

@given('I navigate to the Yahoo login page')
def navigate_to_login(page):
    page.goto('https://login.yahoo.com/')

@when('I enter my Yahoo email and password')
def enter_credentials(page):
    password = os.getenv('EMAIL_PASSWORD')
    page.fill('input[name="username"]', 'testovaci.tester@yahoo.com')
    page.get_by_role("button", name="Next").click()
    page.fill("input[name='password']", password)

@when('I click on the login button')
def click_login(page):
    page.click('button[type="submit"]')

@then('I should see the Yahoo dashboard')
def verify_login(page):
    assert page.url.startswith('https://www.yahoo.com')

@when('I navigate to my contacts')
def navigate_contacts(page):
    page.get_by_role("button", name="Check your mail").click()
    page.wait_for_selector("[data-test-id=\"comms-properties-bar\"]")
    page.wait_for_timeout(1000)
    page.locator("[data-test-id=\"contacts-pane-icon\"]").click()
    page.locator("[data-test-id=\"contact-item-primary-email\"]").click()

@when('I create email')
def create_email(page):
    page.locator("[data-test-id=\"compose-subject\"]").fill('Playwright test')
    page.locator("[data-test-id=\"rte\"] div").fill('Email test body')

@when('I attach a file to the email')
def attach_file(page):
    page.locator("[data-test-id=\"icon-btn-attach\"]").click()
    with page.expect_file_chooser() as fc_info:
        page.get_by_role("button", name="Priložiť súbory z počítača").click()
    file_chooser = fc_info.value
    file_chooser.set_files('e2e/files/sample.txt')

@when('I send the email')
def send_email(page):
    page.click('[data-test-id="compose-send-button"]')

@when('I click on the logout button')
def click_logout(page):
    page.locator('#ybarAccountMenuOpener').hover()
    page.locator('#profile-signout-link').click()

@then('I should be logged out')
def verify_logout(page):
    assert page.url.startswith('https://www.yahoo.com')
