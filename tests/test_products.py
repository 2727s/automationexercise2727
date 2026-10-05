"""Search and product details."""

import allure

from pages.products_page import ProductsPage

pytestmark = allure.feature("Products")


def test_search_finds_blue_top(page):
    products = ProductsPage(page).open()
    products.search("Blue Top").should_list_product("Blue Top")


def test_product_details_show_name_and_price(page):
    details = ProductsPage(page).open().view_product("Blue Top")
    details.should_show_product("Blue Top")
    assert details.price() == "Rs. 500"
