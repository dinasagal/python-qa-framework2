import pytest
import allure
from playwright.sync_api import expect

from config import settings
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


pytestmark = [
    pytest.mark.sanity,
    pytest.mark.source_manual,
    allure.parent_suite("UI Tests"),
    allure.suite("SauceDemo Sanity"),
]

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("sanity", "ui")
@allure.title("Standard user can log in successfully")
@pytest.mark.component_auth
@pytest.mark.type_positive
@pytest.mark.risk_p0
@pytest.mark.speed_fast
def test_standard_user_can_login(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in as standard user"):
        login_page.login_as_standard_user()

    with allure.step("Verify inventory page is loaded"):
        expect(page).to_have_url(settings.inventory_url)
        inventory_page.is_loaded()

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("sanity", "ui")
@allure.title("Inventory is displayed after login")
@pytest.mark.component_inventory
@pytest.mark.type_positive
@pytest.mark.risk_p0
@pytest.mark.speed_fast
def test_inventory_is_displayed_after_login(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in as standard user"):
        login_page.login_as_standard_user()

    with allure.step("Verify inventory is visible"):
        inventory_page.is_loaded()
        assert inventory_page.get_inventory_count() > 0, "Inventory should contain products."

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("sanity", "ui")
@allure.title("User can add item to cart")
@pytest.mark.component_cart
@pytest.mark.type_positive
@pytest.mark.risk_p0
@pytest.mark.speed_fast
def test_user_can_add_item_to_cart(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in as standard user"):
        login_page.login_as_standard_user()

    with allure.step("Add backpack to cart"):
        inventory_page.is_loaded()
        inventory_page.add_backpack_to_cart()

    with allure.step("Verify cart badge shows one item"):
        assert inventory_page.get_cart_badge_count() == 1, "Cart badge should show 1 item."

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("sanity", "ui")
@allure.title("User can open cart and see selected item")
@pytest.mark.component_cart
@pytest.mark.type_positive
@pytest.mark.risk_p0
@pytest.mark.speed_fast
def test_user_can_open_cart_and_see_item(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in as standard user"):
        login_page.login_as_standard_user()

    with allure.step("Add backpack to cart"):
        inventory_page.is_loaded()
        inventory_page.add_backpack_to_cart()

    with allure.step("Open cart"):
        inventory_page.open_cart()

    with allure.step("Verify selected item appears in cart"):
        cart_page.is_loaded()
        assert cart_page.has_item(
            inventory_page.BACKPACK_ITEM_NAME
        ), "Selected item should appear in cart."

@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("sanity", "ui")
@allure.title("User can log out successfully")
@pytest.mark.component_navigation
@pytest.mark.type_positive
@pytest.mark.risk_p1
@pytest.mark.speed_fast
def test_user_can_logout(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in as standard user"):
        login_page.login_as_standard_user()

    with allure.step("Log out from inventory page"):
        inventory_page.is_loaded()
        inventory_page.logout()

    with allure.step("Verify user returns to login page"):
        expect(page).to_have_url(settings.base_url)
        expect(page.locator(login_page.LOGIN_BUTTON)).to_be_visible()


