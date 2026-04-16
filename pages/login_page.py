from playwright.sync_api import Page, expect

from config import settings


class LoginPage:
    URL = settings.base_url

    USERNAME_INPUT = '[data-test="username"]'
    PASSWORD_INPUT = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'
    ERROR_MESSAGE = '[data-test="error"]'

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.URL)
        expect(self.page.locator(self.USERNAME_INPUT)).to_be_visible()
        expect(self.page.locator(self.PASSWORD_INPUT)).to_be_visible()
        expect(self.page.locator(self.LOGIN_BUTTON)).to_be_visible()

    def login(self, username: str, password: str):
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def login_as_standard_user(self):
        self.login(settings.standard_user.username, settings.standard_user.password)

    def login_as_locked_user(self):
        self.login(settings.locked_user.username, settings.locked_user.password)

    def get_error_message(self) -> str:
        return self.page.locator(self.ERROR_MESSAGE).inner_text().strip()