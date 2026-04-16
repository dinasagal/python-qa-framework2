from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def login_standard_user_to_inventory(login_page: LoginPage, inventory_page: InventoryPage):
    login_page.open()
    login_page.login_as_standard_user()
    inventory_page.is_loaded()


def login_locked_user(login_page: LoginPage):
    login_page.open()
    login_page.login_as_locked_user()


def add_backpack_and_open_cart(inventory_page: InventoryPage):
    inventory_page.add_backpack_to_cart()
    inventory_page.open_cart()