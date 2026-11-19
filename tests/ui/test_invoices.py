import pytest
from playwright.sync_api import Page

from pages.invoices_page import InvoicesPage
from pages.customers_page import CustomersPage
from pages.dashboard_page import DashboardPage
from pages.products_page import ProductsPage
from utils.data_factory import customer_data, product_data


@pytest.fixture
def prepared_invoice(logged_in_page) -> tuple[Page, dict[str, str], dict[str, str], InvoicesPage]:
    dashboard = DashboardPage(logged_in_page)

    customer = customer_data()
    dashboard.open_customers()
    CustomersPage(logged_in_page).create_customer(
        customer["name"], customer["email"], customer["phone"]
    )

    product = product_data()
    dashboard.open_products()
    ProductsPage(logged_in_page).create_product(
        product["name"], product["sku"], product["price"], product["stock"]
    )

    dashboard.open_invoices()
    return logged_in_page, customer, product, InvoicesPage(logged_in_page)


@pytest.mark.ui
@pytest.mark.regression
def test_create_invoice_and_validate_gst(prepared_invoice):
    page, customer, product, invoices = prepared_invoice
    invoices.create_invoice(customer["name"], product["name"], "2", "18")

    # Unit price 1000 x quantity 2 = 2000; GST 18% = 360; total = 2360.
    invoices.assert_totals("2000.00", "360.00", "2360.00")
    invoices.save_invoice()
    invoices.assert_invoice_saved(customer["name"], "2360.00")

    DashboardPage(page).open_products()
    ProductsPage(page).assert_stock(product["name"], "23")


@pytest.mark.ui
@pytest.mark.negative
def test_invoice_rejects_zero_quantity(prepared_invoice):
    _, customer, product, invoices = prepared_invoice
    invoices.create_invoice(customer["name"], product["name"], "0", "18")
    invoices.assert_error("Quantity must be greater than zero")


@pytest.mark.ui
@pytest.mark.negative
def test_invoice_rejects_quantity_above_stock(prepared_invoice):
    _, customer, product, invoices = prepared_invoice
    quantity = str(int(product["stock"]) + 1)

    invoices.create_invoice(customer["name"], product["name"], quantity, "18")

    invoices.assert_error("Insufficient stock")
