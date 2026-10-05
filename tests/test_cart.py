"""Cart starts empty in a fresh browser context, then accepts a product."""

import allure

from pages.cart_page import CartPage
from pages.home_page import HomePage

pytestmark = allure.feature("Cart")


def test_cart_is_empty_for_a_new_session(page):
    CartPage(page).open().should_be_empty()


def test_add_product_then_guest_checkout_asks_for_login(page):
    home = HomePage(page).open()
    home.add_listed_product("Blue Top")
    cart = home.view_cart_from_modal()
    cart.should_contain("Blue Top")
    assert cart.quantity_of("Blue Top") == "1"
    cart.proceed_to_checkout().should_ask_guest_to_login()
