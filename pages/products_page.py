from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name = page.get_by_test_id("product-name")
        self.sku = page.get_by_test_id("product-sku")
        self.price = page.get_by_test_id("product-price")
        self.stock = page.get_by_test_id("product-stock")
        self.save_button = page.get_by_test_id("save-product")
        self.error_message = page.get_by_test_id("product-error")

    def create_product(self, name: str, sku: str, price: str, stock: str):
        self.name.fill(name)
        self.sku.fill(sku)
        self.price.fill(price)
        self.stock.fill(stock)
        self.save_button.click()

    def assert_product_visible(self, name: str):
        expect(self.page.get_by_test_id("product-row").filter(has_text=name)).to_be_visible()

    def assert_stock(self, name: str, stock: str):
        product = self.page.get_by_test_id("product-row").filter(has_text=name)
        expect(product).to_contain_text(f"Stock: {stock}")

    def assert_error(self, message: str):
        expect(self.error_message).to_contain_text(message)
