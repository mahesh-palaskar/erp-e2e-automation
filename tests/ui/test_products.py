import pytest
from pages.dashboard_page import DashboardPage
from pages.products_page import ProductsPage
from utils.data_factory import product_data


@pytest.mark.ui
@pytest.mark.regression
def test_create_product(logged_in_page):
    DashboardPage(logged_in_page).open_products()
    products = ProductsPage(logged_in_page)
    data = product_data()
    products.create_product(data["name"], data["sku"], data["price"], data["stock"])
    products.assert_product_visible(data["name"])


@pytest.mark.ui
@pytest.mark.negative
def test_product_rejects_negative_price(logged_in_page):
    DashboardPage(logged_in_page).open_products()
    products = ProductsPage(logged_in_page)
    products.create_product("Invalid Price Item", "BAD-PRICE", "-10", "5")
    products.assert_error("Price must be greater than zero")
