import pytest
import allure
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


pytestmark = [
    pytest.mark.smoke,
    allure.parent_suite("UI Tests"),
    allure.suite("Smoke"),
]


@allure.title("Smoke: Standard user can log in")
@allure.severity(allure.severity_level.CRITICAL)
def test_smoke_login(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Login"):
        login_page.login_as_standard_user()

    with allure.step("Verify inventory page loaded"):
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        inventory_page.is_loaded()


@allure.title("Smoke: User can add item to cart")
@allure.severity(allure.severity_level.CRITICAL)
def test_smoke_add_to_cart(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    with allure.step("Add item to cart"):
        inventory_page.add_backpack_to_cart()

    with allure.step("Verify cart badge = 1"):
        assert inventory_page.get_cart_badge_count() == 1


@allure.title("Smoke: Cart badge updates correctly")
def test_smoke_cart_badge(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    inventory_page.add_backpack_to_cart()
    inventory_page.remove_backpack_from_cart()

    with allure.step("Verify cart badge returns to 0"):
        assert inventory_page.get_cart_badge_count() == 0


@allure.title("Smoke: User can logout")
def test_smoke_logout(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    with allure.step("Logout"):
        inventory_page.logout()

    with allure.step("Verify back on login page"):
        expect(page).to_have_url("https://www.saucedemo.com/")