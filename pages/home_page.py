"""Landing page: featured products, categories, brands, and subscription."""

from playwright.sync_api import expect

from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    def open(self):
        super().open(self.PATH)
        return self

    def should_be_open(self):
        expect(self.page).to_have_title("Automation Exercise")
        # The slider repeats this heading once per slide.
        expect(
            self.page.get_by_role(
                "heading", name="Full-Fledged practice website for Automation Engineers"
            ).first
        ).to_be_visible()
        return self

    def open_category(self, group: str, category: str):
        """Expand a sidebar group (Women, Men, Kids) and open a category."""
        sidebar = self.page.locator("#accordian")
        sidebar.get_by_role("link", name=group, exact=True).click()
        sidebar.locator(f"#{group}").get_by_role(
            "link", name=category, exact=True
        ).click()
        from pages.products_page import ProductsPage

        return ProductsPage(self.page)

    def open_brand(self, brand: str):
        self.page.locator(".brands-name").get_by_role("link", name=brand).click()
        from pages.products_page import ProductsPage

        return ProductsPage(self.page)

    def subscribe(self, email: str):
        # The site's input id is misspelled: susbscribe_email.
        self.page.locator("#susbscribe_email").fill(email)
        self.page.locator("#subscribe").click()
        expect(self.page.locator("#success-subscribe")).to_be_visible()
        return self
