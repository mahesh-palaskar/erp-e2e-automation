from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_test_id("dashboard-heading")
        self.customers_link = page.get_by_test_id("nav-customers")
        self.products_link = page.get_by_test_id("nav-products")
        self.invoices_link = page.get_by_test_id("nav-invoices")
        self.logout_button = page.get_by_test_id("logout-button")

    def assert_loaded(self):
        expect(self.heading).to_have_text("ERP Dashboard")

    def open_customers(self):
        self.customers_link.click()

    def open_products(self):
        self.products_link.click()

    def open_invoices(self):
        self.invoices_link.click()

    def logout(self):
        self.logout_button.click()
