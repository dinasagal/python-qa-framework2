from playwright.sync_api import Page, expect


class InventoryPage:
    INVENTORY_CONTAINER = '[data-test="inventory-container"]'
    INVENTORY_ITEMS = '[data-test="inventory-item"]'
    CART_LINK = '[data-test="shopping-cart-link"]'
    CART_BADGE = '[data-test="shopping-cart-badge"]'
    MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = '[data-test="logout-sidebar-link"]'

    BACKPACK_ADD_BUTTON = '[data-test="add-to-cart-sauce-labs-backpack"]'
    BACKPACK_REMOVE_BUTTON = '[data-test="remove-sauce-labs-backpack"]'
    BACKPACK_ITEM_NAME = "Sauce Labs Backpack"

    def __init__(self, page: Page):
        self.page = page

    def is_loaded(self):
        expect(self.page.locator(self.INVENTORY_CONTAINER)).to_be_visible()
        expect(self.page.locator(self.INVENTORY_ITEMS).first).to_be_visible()

    def get_inventory_count(self) -> int:
        return self.page.locator(self.INVENTORY_ITEMS).count()

    def add_backpack_to_cart(self):
        self.page.click(self.BACKPACK_ADD_BUTTON)

    def remove_backpack_from_cart(self):
        self.page.click(self.BACKPACK_REMOVE_BUTTON)

    def get_cart_badge_count(self) -> int:
        badge = self.page.locator(self.CART_BADGE)
        if badge.count() == 0 or not badge.is_visible():
            return 0
        return int(badge.inner_text().strip())

    def open_cart(self):
        self.page.click(self.CART_LINK)

    def open_menu(self):
        self.page.click(self.MENU_BUTTON)

    def logout(self):
        self.open_menu()
        expect(self.page.locator(self.LOGOUT_LINK)).to_be_visible()
        self.page.click(self.LOGOUT_LINK)