import pytest
from pages.dashboard_page import DashboardPage
from pages.customers_page import CustomersPage
from utils.data_factory import customer_data


@pytest.mark.ui
@pytest.mark.regression
def test_create_customer(logged_in_page):
    dashboard = DashboardPage(logged_in_page)
    dashboard.open_customers()

    customers = CustomersPage(logged_in_page)
    data = customer_data()
    customers.create_customer(data["name"], data["email"], data["phone"])
    customers.assert_customer_visible(data["name"])


@pytest.mark.ui
@pytest.mark.negative
def test_customer_requires_name(logged_in_page):
    DashboardPage(logged_in_page).open_customers()
    customers = CustomersPage(logged_in_page)
    customers.create_customer("", "missingname@example.com", "9876543210")
    customers.assert_error("Customer name is required")
