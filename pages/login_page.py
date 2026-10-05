"""Login and the start of signup. Both forms live on /login."""

from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/login"

    def open(self):
        super().open(self.PATH)
        return self

    def should_be_open(self):
        expect(
            self.page.get_by_role("heading", name="Login to your account")
        ).to_be_visible()
        expect(
            self.page.get_by_role("heading", name="New User Signup!")
        ).to_be_visible()
        return self

    def login(self, email: str, password: str):
        self.page.locator("[data-qa='login-email']").fill(email)
        self.page.locator("[data-qa='login-password']").fill(password)
        self.page.locator("[data-qa='login-button']").click()
        return self

    def should_show_login_error(self):
        expect(
            self.page.get_by_text("Your email or password is incorrect!")
        ).to_be_visible()
        return self

    def should_be_logged_in_as(self, name: str):
        expect(self.header.get_by_text(f"Logged in as {name}")).to_be_visible()
        return self

    def logout(self):
        self.header.get_by_role("link", name="Logout").click()
        return self

    def start_signup(self, name: str, email: str):
        self.page.locator("[data-qa='signup-name']").fill(name)
        self.page.locator("[data-qa='signup-email']").fill(email)
        self.page.locator("[data-qa='signup-button']").click()
        from pages.signup_page import SignupPage

        return SignupPage(self.page)

    def should_show_signup_error(self):
        expect(self.page.get_by_text("Email Address already exist!")).to_be_visible()
        return self
