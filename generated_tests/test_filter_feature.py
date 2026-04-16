import pytest
import allure

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


pytestmark = [
    pytest.mark.regression,
    pytest.mark.component_sort,
    pytest.mark.source_generated,
    allure.parent_suite("UI Tests"),
    allure.suite("Generated Filter"),
]


@allure.title("Generated Filter: Products can be sorted by name from A to Z")
@pytest.mark.type_positive
@pytest.mark.risk_p1
@pytest.mark.speed_fast
def test_filter_name_a_to_z(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in as standard user"):
        login_page.login_as_standard_user()

    with allure.step("Verify inventory page is loaded"):
        inventory_page.is_loaded()

    with allure.step("Select name filter from A to Z"):
        inventory_page.select_sort("az")

    names = inventory_page.get_item_names()

    with allure.step("Verify product names are sorted ascending"):
        assert names == sorted(names), "Product names should be sorted from A to Z."


@allure.title("Generated Filter: Products can be sorted by name from Z to A")
@pytest.mark.type_positive
@pytest.mark.risk_p1
@pytest.mark.speed_fast
def test_filter_name_z_to_a(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in as standard user"):
        login_page.login_as_standard_user()

    with allure.step("Verify inventory page is loaded"):
        inventory_page.is_loaded()

    with allure.step("Select name filter from Z to A"):
        inventory_page.select_sort("za")

    names = inventory_page.get_item_names()

    with allure.step("Verify product names are sorted descending"):
        assert names == sorted(names, reverse=True), "Product names should be sorted from Z to A."


@allure.title("Generated Filter: Products can be sorted by price from low to high")
@pytest.mark.type_positive
@pytest.mark.risk_p1
@pytest.mark.speed_fast
def test_filter_price_low_to_high(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in as standard user"):
        login_page.login_as_standard_user()

    with allure.step("Verify inventory page is loaded"):
        inventory_page.is_loaded()

    with allure.step("Select price filter from low to high"):
        inventory_page.select_sort("lohi")

    prices = inventory_page.get_item_prices()

    with allure.step("Verify prices are sorted ascending"):
        assert prices == sorted(prices), "Prices should be sorted from low to high."


@allure.title("Generated Filter: Products can be sorted by price from high to low")
@pytest.mark.type_positive
@pytest.mark.risk_p1
@pytest.mark.speed_fast
def test_filter_price_high_to_low(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in as standard user"):
        login_page.login_as_standard_user()

    with allure.step("Verify inventory page is loaded"):
        inventory_page.is_loaded()

    with allure.step("Select price filter from high to low"):
        inventory_page.select_sort("hilo")

    prices = inventory_page.get_item_prices()

    with allure.step("Verify prices are sorted descending"):
        assert prices == sorted(prices, reverse=True), "Prices should be sorted from high to low."
