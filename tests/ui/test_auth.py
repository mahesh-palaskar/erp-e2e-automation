import pytest
from config.settings import APP_PASSWORD, APP_USERNAME
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login_opens_dashboard(page, app_base_url):
    page.goto(app_base_url)
    LoginPage(page).login(APP_USERNAME, APP_PASSWORD)
    DashboardPage(page).assert_loaded()


@pytest.mark.ui
@pytest.mark.negative
def test_invalid_login_shows_error(page, app_base_url):
    page.goto(app_base_url)
    login = LoginPage(page)
    login.login("wrong-user", "wrong-password")
    login.assert_login_error("Invalid username or password")
