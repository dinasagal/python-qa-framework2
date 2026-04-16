import pytest
import allure
from playwright.sync_api import expect

from config import settings
from flows import login_standard_user_to_inventory
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


pytestmark = [
    pytest.mark.smoke,
    pytest.mark.source_manual,
    allure.parent_suite("UI Tests"),
    allure.suite("Smoke"),
]


@allure.title("Smoke: Standard user can log in")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.component_auth
@pytest.mark.type_positive
@pytest.mark.risk_p0
@pytest.mark.speed_fast
def test_smoke_login(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page and login"):
        login_standard_user_to_inventory(login_page, inventory_page)

    with allure.step("Verify inventory page loaded"):
        expect(page).to_have_url(settings.inventory_url)


@allure.title("Smoke: User can add item to cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.component_cart
@pytest.mark.type_positive
@pytest.mark.risk_p0
@pytest.mark.speed_fast
def test_smoke_add_to_cart(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_standard_user_to_inventory(login_page, inventory_page)

    with allure.step("Add item to cart"):
        inventory_page.add_backpack_to_cart()

    with allure.step("Verify cart badge = 1"):
        assert inventory_page.get_cart_badge_count() == 1


@allure.title("Smoke: Cart badge updates correctly")
@pytest.mark.component_cart
@pytest.mark.type_edge
@pytest.mark.risk_p1
@pytest.mark.speed_fast
def test_smoke_cart_badge(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_standard_user_to_inventory(login_page, inventory_page)

    inventory_page.add_backpack_to_cart()
    inventory_page.remove_backpack_from_cart()

    with allure.step("Verify cart badge returns to 0"):
        assert inventory_page.get_cart_badge_count() == 0


@allure.title("Smoke: User can logout")
@pytest.mark.component_navigation
@pytest.mark.type_positive
@pytest.mark.risk_p1
@pytest.mark.speed_fast
def test_smoke_logout(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_standard_user_to_inventory(login_page, inventory_page)

    with allure.step("Logout"):
        inventory_page.logout()

    with allure.step("Verify back on login page"):
        expect(page).to_have_url(settings.base_url)