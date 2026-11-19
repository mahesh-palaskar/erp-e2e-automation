from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CustomersPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name = page.get_by_test_id("customer-name")
        self.email = page.get_by_test_id("customer-email")
        self.phone = page.get_by_test_id("customer-phone")
        self.save_button = page.get_by_test_id("save-customer")
        self.success_message = page.get_by_test_id("customer-success")
        self.error_message = page.get_by_test_id("customer-error")
        self.search = page.get_by_test_id("customer-search")

    def create_customer(self, name: str, email: str, phone: str):
        self.name.fill(name)
        self.email.fill(email)
        self.phone.fill(phone)
        self.save_button.click()

    def assert_customer_visible(self, name: str):
        expect(self.page.get_by_test_id("customer-row").filter(has_text=name)).to_be_visible()

    def assert_error(self, message: str):
        expect(self.error_message).to_contain_text(message)

    def search_customer(self, name: str):
        self.search.fill(name)
