from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def expect_visible(self, locator):
        expect(locator).to_be_visible()

    def click(self, locator):
        locator.click()

    def fill(self, locator, value: str):
        locator.fill(value)
