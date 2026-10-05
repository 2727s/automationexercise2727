"""Single product page: price, quantity, and reviews."""

from playwright.sync_api import expect

from pages.base_page import BasePage


class ProductDetailsPage(BasePage):
    def should_show_product(self, name: str):
        info = self.page.locator(".product-information")
        expect(info.get_by_role("heading", name=name)).to_be_visible()
        return self

    def price(self) -> str:
        return self.page.locator(".product-information span span").inner_text().strip()

    def set_quantity(self, quantity: int):
        field = self.page.locator("#quantity")
        field.fill(str(quantity))
        return self

    def add_to_cart(self):
        self.page.get_by_role("button", name="Add to cart").click()
        return self

    def write_review(self, name: str, email: str, review: str):
        self.page.locator("#name").fill(name)
        self.page.locator("#email").fill(email)
        self.page.locator("#review").fill(review)
        self.page.locator("#button-review").click()
        expect(self.page.locator("#review-section .alert-success")).to_be_visible()
        return self
