import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


pytestmark = pytest.mark.sanity


def test_standard_user_can_login(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    inventory_page.is_loaded()


def test_inventory_is_displayed_after_login(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    inventory_page.is_loaded()
    assert inventory_page.get_inventory_count() > 0, "Inventory should contain products."


def test_user_can_add_item_to_cart(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    inventory_page.is_loaded()
    inventory_page.add_backpack_to_cart()

    assert inventory_page.get_cart_badge_count() == 1, "Cart badge should show 1 item."


def test_user_can_open_cart_and_see_item(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    inventory_page.is_loaded()
    inventory_page.add_backpack_to_cart()
    inventory_page.open_cart()

    cart_page.is_loaded()
    assert cart_page.has_item(
        inventory_page.BACKPACK_ITEM_NAME
    ), "Selected item should appear in cart."


def test_user_can_logout(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.open()
    login_page.login_as_standard_user()

    inventory_page.is_loaded()
    inventory_page.logout()

    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(page.locator(login_page.LOGIN_BUTTON)).to_be_visible()