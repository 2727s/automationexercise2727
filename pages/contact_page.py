"""Contact Us form."""

from playwright.sync_api import expect

from pages.base_page import BasePage


class ContactPage(BasePage):
    PATH = "/contact_us"

    def open(self):
        super().open(self.PATH)
        return self

    def should_be_open(self):
        expect(self.page.get_by_role("heading", name="Get In Touch")).to_be_visible()
        return self

    def submit_message(self, name: str, email: str, subject: str, message: str):
        self.page.locator("[data-qa='name']").fill(name)
        self.page.locator("[data-qa='email']").fill(email)
        self.page.locator("[data-qa='subject']").fill(subject)
        self.page.locator("[data-qa='message']").fill(message)
        # The site asks for a confirm dialog before it posts the form.
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.locator("[data-qa='submit-button']").click()
        expect(self.page.locator(".status.alert-success")).to_contain_text("Success!")
        return self
