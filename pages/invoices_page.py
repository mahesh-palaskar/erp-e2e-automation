from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class InvoicesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.customer = page.get_by_test_id("invoice-customer")
        self.product = page.get_by_test_id("invoice-product")
        self.quantity = page.get_by_test_id("invoice-quantity")
        self.gst_rate = page.get_by_test_id("invoice-gst")
        self.calculate_button = page.get_by_test_id("calculate-invoice")
        self.subtotal = page.get_by_test_id("invoice-subtotal")
        self.gst_amount = page.get_by_test_id("invoice-gst-amount")
        self.total = page.get_by_test_id("invoice-total")
        self.save_button = page.get_by_test_id("save-invoice")
        self.success_message = page.get_by_test_id("invoice-success")
        self.error_message = page.get_by_test_id("invoice-error")

    def create_invoice(self, customer: str, product: str, quantity: str, gst_rate: str):
        self.customer.select_option(label=customer)
        self.product.select_option(label=product)
        self.quantity.fill(quantity)
        self.gst_rate.select_option(gst_rate)
        self.calculate_button.click()

    def assert_totals(self, subtotal: str, gst: str, total: str):
        expect(self.subtotal).to_have_text(subtotal)
        expect(self.gst_amount).to_have_text(gst)
        expect(self.total).to_have_text(total)

    def save_invoice(self):
        self.save_button.click()

    def assert_invoice_saved(self, customer_name: str, total: str):
        invoice = self.page.get_by_test_id("invoice-row").filter(has_text=customer_name)
        expect(invoice).to_be_visible()
        expect(invoice).to_contain_text(total)

    def assert_error(self, message: str):
        expect(self.error_message).to_have_text(message)
