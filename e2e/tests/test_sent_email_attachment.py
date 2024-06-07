from dotenv import load_dotenv
import os
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import sync_playwright, Page

load_dotenv()

scenarios('send_email_with_attachment.feature')

new_page = None

def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        browser.close()

@given('I navigate to the Yahoo login page')
def navigate_to_login(page: Page):
    page.goto('https://login.yahoo.com/')

@when('I enter my Yahoo email and password')
def enter_credentials(page: Page):
    password = os.getenv('EMAIL_PASSWORD')
    page.fill('input[name="username"]', 'testovaci.tester@yahoo.com')
    page.get_by_role("button", name="Next").click()
    page.fill("input[name='password']", password)

@when('I click on the login button')
def click_login(page: Page):
    page.click('button[type="submit"]')

@then('I should see the Yahoo dashboard')
def verify_login(page: Page):
    assert page.url.startswith('https://www.yahoo.com')

@when('I navigate to my contacts')
def navigate_to_contacts(page: Page):
    global new_page
    with page.context.expect_page() as new_page_info:
        page.get_by_role("button", name="Check your mail").click()
    
    new_page = new_page_info.value
    new_page.wait_for_selector("[data-test-id=\"comms-properties-bar\"]")
    new_page.wait_for_timeout(1000)
    new_page.locator("[data-test-id=\"contacts-pane-icon\"]").click()
    new_page.locator("[data-test-id=\"contact-item-primary-email\"]").click()

@when('I create email')
def create_email():
    global new_page
    new_page.locator("[data-test-id=\"compose-subject\"]").fill('Playwright test')
    new_page.locator("[data-test-id=\"rte\"] div").fill('Email test body')

@when('I attach a file to the email')
def attach_file():
    global new_page
    new_page.locator("[data-test-id=\"icon-btn-attach\"]").click()
    with new_page.expect_file_chooser() as fc_info:
        new_page.get_by_role("button", name="Priložiť súbory z počítača").click()
    file_chooser = fc_info.value
    file_chooser.set_files('e2e/files/sample.txt')

@when('I send the email')
def send_email():
    global new_page
    new_page.click('[data-test-id="compose-send-button"]')

@when('I click on the logout button')
def click_logout():
    global new_page
    new_page.locator('#ybarAccountMenuOpener').hover()
    new_page.locator('#profile-signout-link').click()

@then('I should be logged out')
def verify_logout():
    global new_page
    assert new_page.url.startswith('https://www.yahoo.com')
