"""Contact form."""

import allure

from pages.contact_page import ContactPage

pytestmark = allure.feature("Contact")


def test_contact_page_loads(page):
    ContactPage(page).open().should_be_open()


def test_contact_form_submits(page):
    contact = ContactPage(page).open()
    contact.submit_message(
        name="QA Tester",
        email="qa.tester@example.com",
        subject="Framework check",
        message="Hello from the Playwright suite.",
    )
