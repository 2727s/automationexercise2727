"""Product listing and search."""

from playwright.sync_api import expect

from pages.base_page import BasePage


class ProductsPage(BasePage):
    PATH = "/products"

    def open(self):
        super().open(self.PATH)
        return self

    def should_be_open(self):
        expect(self.page).to_have_url("/products")
        expect(self.page.get_by_role("heading", name="All Products")).to_be_visible()
        return self

    def search(self, text: str):
        self.page.locator("#search_product").fill(text)
        self.page.locator("#submit_search").click()
        expect(
            self.page.get_by_role("heading", name="Searched Products")
        ).to_be_visible()
        return self

    def should_list_product(self, name: str):
        expect(
            self.page.locator(".features_items").get_by_text(name).first
        ).to_be_visible()
        return self

    def view_product(self, name: str):
        card = (
            self.page.locator(".features_items .product-image-wrapper")
            .filter(has_text=name)
            .first
        )
        card.get_by_role("link", name="View Product").click()
        from pages.product_details_page import ProductDetailsPage

        return ProductDetailsPage(self.page)
