"""Login form. Unknown accounts come from the faker_letters pair in .env."""

import allure

from helper import get_login_password
from pages.login_page import LoginPage

pytestmark = allure.feature("Login")


def test_login_page_shows_both_forms(page):
    LoginPage(page).open().should_be_open()


def test_unknown_user_sees_login_error(page):
    email, password = get_login_password()
    login = LoginPage(page).open()
    login.login(email, password)
    login.should_show_login_error()


def test_empty_login_fields_stay_on_login_page(page):
    login = LoginPage(page).open()
    login.login("", "")
    login.should_block_empty_login()
