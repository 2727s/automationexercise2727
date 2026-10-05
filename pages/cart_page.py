"""Shopping cart."""

from playwright.sync_api import expect

from pages.base_page import BasePage


class CartPage(BasePage):
    PATH = "/view_cart"

    def open(self):
        super().open(self.PATH)
        return self

    def should_be_open(self):
        expect(self.page.get_by_role("link", name="Shopping Cart")).to_be_visible()
        return self

    def should_be_empty(self):
        expect(self.page.get_by_text("Cart is empty!")).to_be_visible()
        return self

    def should_contain(self, name: str):
        row = self._row(name)
        expect(row).to_be_visible()
        return self

    def quantity_of(self, name: str) -> str:
        return self._row(name).locator(".cart_quantity").inner_text().strip()

    def remove(self, name: str):
        self._row(name).locator(".cart_quantity_delete").click()
        expect(self._row(name)).to_have_count(0)
        return self

    def proceed_to_checkout(self):
        """Click checkout. Guests see a Register / Login modal instead of checkout."""
        self.page.get_by_text("Proceed To Checkout").click()
        return self

    def should_ask_guest_to_login(self):
        modal = self.page.locator("#checkoutModal")
        expect(modal).to_be_visible()
        expect(modal.get_by_role("link", name="Register / Login")).to_be_visible()
        return self

    def _row(self, name: str):
        return self.page.locator("#cart_info_table tbody tr").filter(has_text=name)
