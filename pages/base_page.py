"""Shared navigation and cart-modal actions used by every page."""

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        # Header nav is shared; footer links repeat the same names.
        self.header = page.locator("#header")

    def open(self, path: str):
        # domcontentloaded avoids waiting on leftover third-party scripts.
        self.page.goto(path, wait_until="domcontentloaded")
        return self

    def go_home(self):
        self.header.get_by_role("link", name="Home").click()
        from pages.home_page import HomePage

        return HomePage(self.page)

    def go_to_products(self):
        self.header.get_by_role("link", name="Products").click()
        from pages.products_page import ProductsPage

        return ProductsPage(self.page)

    def go_to_cart(self):
        self.header.get_by_role("link", name="Cart").click()
        from pages.cart_page import CartPage

        return CartPage(self.page)

    def go_to_login(self):
        self.header.get_by_role("link", name="Signup / Login").click()
        from pages.login_page import LoginPage

        return LoginPage(self.page)

    def go_to_contact(self):
        self.header.get_by_role("link", name="Contact us").click()
        from pages.contact_page import ContactPage

        return ContactPage(self.page)

    def add_listed_product(self, name: str):
        """Add a product card from a home or products grid."""
        card = (
            self.page.locator(".features_items .product-image-wrapper")
            .filter(has_text=name)
            .first
        )
        # Two Add to cart controls exist. The info one is visible without hover.
        card.locator(".productinfo a.add-to-cart").click()
        return self

    def view_cart_from_modal(self):
        """Confirm the 'Added!' dialog and open the cart."""
        modal = self.page.locator("#cartModal")
        expect(modal).to_be_visible()
        modal.get_by_role("link", name="View Cart").click()
        from pages.cart_page import CartPage

        return CartPage(self.page)

    def continue_shopping(self):
        self.page.locator("#cartModal").get_by_role(
            "button", name="Continue Shopping"
        ).click()
        return self
