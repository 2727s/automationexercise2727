"""Signup form. Run headed and slow to read the name and postcode."""

import allure
from playwright.sync_api import expect

from helper import get_name, get_postcode
from helpers.users import get_login_password
from pages.login_page import LoginPage

pytestmark = allure.feature("Signup")


def test_signup_shows_name_and_postcode(page):
    first_name, last_name = get_name()
    postcode = get_postcode()
    email, password = get_login_password()
    print(f"name={first_name} {last_name} postcode={postcode}")

    signup = LoginPage(page).open().start_signup(f"{first_name} {last_name}", email)
    signup.should_be_open().fill_account(
        password=password,
        first_name=first_name,
        last_name=last_name,
        address="1 Test Street",
        country="United States",
        state="Texas",
        city="Austin",
        zipcode=postcode,
        mobile="5551234567",
    )

    # Scroll each field into view and leave it on screen long enough to read.
    page.locator("#first_name").scroll_into_view_if_needed()
    page.wait_for_timeout(2500)
    page.locator("#zipcode").scroll_into_view_if_needed()
    page.wait_for_timeout(2500)

    expect(page.locator("#first_name")).to_have_value(first_name)
    expect(page.locator("#last_name")).to_have_value(last_name)
    expect(page.locator("#zipcode")).to_have_value(postcode)
