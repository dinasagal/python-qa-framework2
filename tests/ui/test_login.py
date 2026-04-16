from config import settings
from pages.login_page import LoginPage


def test_successful_login(page):
    login_page = LoginPage(page)

    login_page.open()

    login_page.login_as_standard_user()

    assert page.url == settings.inventory_url