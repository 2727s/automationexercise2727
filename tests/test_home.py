"""Smoke checks for the landing page."""

import allure

from pages.home_page import HomePage

pytestmark = allure.feature("Home")


def test_home_page_loads(page):
    home = HomePage(page).open()
    home.should_be_open()


def test_home_navigation_reaches_products(page):
    products = HomePage(page).open().go_to_products()
    products.should_be_open()
