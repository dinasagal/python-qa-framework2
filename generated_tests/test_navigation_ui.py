import pytest
import allure
from playwright.sync_api import expect

from config import settings
from flows import add_backpack_and_open_cart
from flows import login_standard_user_to_inventory
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_detail_page import ProductDetailPage


pytestmark = [
    pytest.mark.regression,
    pytest.mark.component_navigation,
    pytest.mark.source_generated,
    allure.parent_suite("UI Tests"),
    allure.suite("Generated Navigation & UI"),
]


# ---------------------------------------------------------------------------
# TC1
# ---------------------------------------------------------------------------

@allure.title("Generated Navigation: User navigates to cart page from inventory")
@pytest.mark.type_positive
@pytest.mark.risk_p1
@pytest.mark.speed_fast
def test_generated_navigate_to_cart_from_inventory(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    with allure.step("Open login page and log in as standard user"):
        login_standard_user_to_inventory(login_page, inventory_page)

    with allure.step("Open cart"):
        inventory_page.open_cart()

    with allure.step("Verify cart page is loaded"):
        cart_page.is_loaded()


# ---------------------------------------------------------------------------
# TC2
# ---------------------------------------------------------------------------

@allure.title("Generated Navigation: User navigates back to inventory from cart")
@pytest.mark.type_positive
@pytest.mark.risk_p1
@pytest.mark.speed_fast
def test_generated_navigate_back_to_inventory_from_cart(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    with allure.step("Open login page and log in as standard user"):
        login_standard_user_to_inventory(login_page, inventory_page)

    with allure.step("Add backpack to cart and open cart"):
        add_backpack_and_open_cart(inventory_page)

    with allure.step("Verify cart page is loaded"):
        cart_page.is_loaded()

    with allure.step("Navigate back to inventory"):
        page.go_back()

    with allure.step("Verify inventory page is loaded"):
        inventory_page.is_loaded()


# ---------------------------------------------------------------------------
# TC3
# ---------------------------------------------------------------------------

@allure.title("Generated Navigation: User returns to login page after logout")
@pytest.mark.type_positive
@pytest.mark.risk_p1
@pytest.mark.speed_fast
def test_generated_logout_returns_to_login(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page and log in as standard user"):
        login_standard_user_to_inventory(login_page, inventory_page)

    with allure.step("Log out from inventory page"):
        inventory_page.logout()

    with allure.step("Verify user is back on the login page"):
        expect(page).to_have_url(settings.base_url)
        expect(page.locator(login_page.LOGIN_BUTTON)).to_be_visible()


# ---------------------------------------------------------------------------
# TC4
# ---------------------------------------------------------------------------

@allure.title("Generated Navigation: Cart page is accessible with no items")
@pytest.mark.type_edge
@pytest.mark.risk_p2
@pytest.mark.speed_fast
def test_generated_cart_accessible_with_no_items(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    with allure.step("Open login page and log in as standard user"):
        login_standard_user_to_inventory(login_page, inventory_page)

    with allure.step("Open cart without adding items"):
        inventory_page.open_cart()

    with allure.step("Verify cart page loads"):
        cart_page.is_loaded()

    with allure.step("Verify cart contains zero items"):
        assert cart_page.get_cart_count() == 0, "Cart should be empty when no items were added."


# ---------------------------------------------------------------------------
# TC5
# ---------------------------------------------------------------------------

@allure.title("Generated Navigation: Cart badge is absent when cart is empty")
@pytest.mark.type_edge
@pytest.mark.risk_p2
@pytest.mark.speed_fast
def test_generated_cart_badge_absent_when_empty(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page and log in as standard user"):
        login_standard_user_to_inventory(login_page, inventory_page)

    with allure.step("Verify cart badge count is 0"):
        assert inventory_page.get_cart_badge_count() == 0, \
            "Cart badge should not be visible when no items are in the cart."


# ---------------------------------------------------------------------------
# TC6  (unblocked: InventoryPage.close_menu / is_menu_open / is_menu_closed added)
# ---------------------------------------------------------------------------

@allure.title("Generated Navigation: Side menu opens and closes")
@pytest.mark.type_positive
@pytest.mark.risk_p2
@pytest.mark.speed_fast
def test_generated_side_menu_opens_and_closes(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page and log in as standard user"):
        login_standard_user_to_inventory(login_page, inventory_page)

    with allure.step("Open side menu"):
        inventory_page.open_menu()

    with allure.step("Verify side menu is open"):
        inventory_page.is_menu_open()

    with allure.step("Close side menu"):
        inventory_page.close_menu()

    with allure.step("Verify side menu is closed"):
        inventory_page.is_menu_closed()


# ---------------------------------------------------------------------------
# TC7  (unblocked: ProductDetailPage added to pages/)
# ---------------------------------------------------------------------------

@allure.title("Generated Navigation: Clicking a product opens its detail page")
@pytest.mark.type_positive
@pytest.mark.risk_p2
@pytest.mark.speed_fast
def test_generated_product_detail_page_loads(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    detail_page = ProductDetailPage(page)

    target_product = "Sauce Labs Backpack"

    with allure.step("Open login page and log in as standard user"):
        login_standard_user_to_inventory(login_page, inventory_page)

    with allure.step(f"Click on product: {target_product}"):
        inventory_page.click_product_by_name(target_product)

    with allure.step("Verify product detail page is loaded"):
        detail_page.is_loaded()

    with allure.step("Verify product name matches the clicked item"):
        assert detail_page.get_product_name() == target_product, \
            f"Expected product name '{target_product}' on detail page."
