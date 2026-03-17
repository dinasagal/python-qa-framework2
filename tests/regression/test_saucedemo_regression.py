import pytest
import allure

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


pytestmark = [
    pytest.mark.regression,
    allure.parent_suite("UI Tests"),
    allure.suite("Regression"),
]


@allure.title("Regression: Login fails with invalid credentials")
def test_login_invalid_user(page):
    login_page = LoginPage(page)

    login_page.open()

    with allure.step("Login with invalid credentials"):
        login_page.login("invalid_user", "wrong_password")

    with allure.step("Verify error message is displayed"):
        assert "Epic sadface" in login_page.get_error_message()


@allure.title("Regression: Locked user cannot login")
def test_locked_user_login(page):
    login_page = LoginPage(page)

    login_page.open()

    with allure.step("Login with locked user"):
        login_page.login("locked_out_user", "secret_sauce")

    with allure.step("Verify locked out error"):
        assert "locked out" in login_page.get_error_message().lower()


@allure.title("Regression: User can remove item from cart")
def test_remove_item_from_cart(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    inventory_page.add_backpack_to_cart()
    inventory_page.remove_backpack_from_cart()

    with allure.step("Verify cart is empty"):
        assert inventory_page.get_cart_badge_count() == 0


@allure.title("Regression: Multiple items can be added to cart")
def test_add_multiple_items(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    with allure.step("Add multiple items"):
        page.click('[data-test="add-to-cart-sauce-labs-backpack"]')
        page.click('[data-test="add-to-cart-sauce-labs-bike-light"]')

    with allure.step("Verify cart badge = 2"):
        assert inventory_page.get_cart_badge_count() == 2


@allure.title("Regression: Cart persists after navigation")
def test_cart_persistence(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    inventory_page.add_backpack_to_cart()
    inventory_page.open_cart()
    cart_page.is_loaded()

    page.go_back()

    with allure.step("Verify cart still has item"):
        assert inventory_page.get_cart_badge_count() == 1


@allure.title("Regression: Sort products low to high")
def test_sort_low_to_high(page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    with allure.step("Select sort low to high"):
        page.select_option('[data-test="product-sort-container"]', "lohi")

    prices = page.locator('[data-test="inventory-item-price"]').all_inner_texts()
    prices = [float(p.replace("$", "")) for p in prices]

    with allure.step("Verify prices sorted ascending"):
        assert prices == sorted(prices)


@allure.title("Regression: Sort products high to low")
def test_sort_high_to_low(page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    with allure.step("Select sort high to low"):
        page.select_option('[data-test="product-sort-container"]', "hilo")

    prices = page.locator('[data-test="inventory-item-price"]').all_inner_texts()
    prices = [float(p.replace("$", "")) for p in prices]

    with allure.step("Verify prices sorted descending"):
        assert prices == sorted(prices, reverse=True)