"""Account information form shown after a new signup email is accepted."""

from playwright.sync_api import expect

from pages.base_page import BasePage


class SignupPage(BasePage):
    def should_be_open(self):
        expect(self.page.get_by_text("Enter Account Information")).to_be_visible()
        return self

    def fill_account(
        self,
        *,
        password: str,
        first_name: str,
        last_name: str,
        address: str,
        country: str,
        state: str,
        city: str,
        zipcode: str,
        mobile: str,
        title: str = "Mr",
        day: str = "1",
        month: str = "1",
        year: str = "2000",
    ):
        title_id = "#id_gender1" if title == "Mr" else "#id_gender2"
        self.page.locator(title_id).check()
        self.page.locator("#password").fill(password)
        self.page.locator("#days").select_option(day)
        self.page.locator("#months").select_option(month)
        self.page.locator("#years").select_option(year)
        self.page.locator("#first_name").fill(first_name)
        self.page.locator("#last_name").fill(last_name)
        self.page.locator("#address1").fill(address)
        self.page.locator("#country").select_option(label=country)
        self.page.locator("#state").fill(state)
        self.page.locator("#city").fill(city)
        self.page.locator("#zipcode").fill(zipcode)
        self.page.locator("#mobile_number").fill(mobile)
        return self

    def create_account(self):
        self.page.locator("[data-qa='create-account']").click()
        expect(self.page.locator("[data-qa='account-created']")).to_have_text(
            "Account Created!"
        )
        return self

    def continue_(self):
        self.page.locator("[data-qa='continue-button']").click()
        from pages.home_page import HomePage

        return HomePage(self.page)
