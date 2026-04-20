from playwright.sync_api import Page, expect


class InventoryPage:
    INVENTORY_CONTAINER = '[data-test="inventory-container"]'
    INVENTORY_ITEMS = '[data-test="inventory-item"]'
    INVENTORY_ITEM_NAMES = '[data-test="inventory-item-name"]'
    INVENTORY_ITEM_PRICES = '[data-test="inventory-item-price"]'
    SORT_DROPDOWN = '[data-test="product-sort-container"]'
    CART_LINK = '[data-test="shopping-cart-link"]'
    CART_BADGE = '[data-test="shopping-cart-badge"]'
    MENU_BUTTON = "#react-burger-menu-btn"
    MENU_CLOSE_BUTTON = "#react-burger-cross-btn"
    MENU_WRAPPER = ".bm-menu-wrap"
    LOGOUT_LINK = '[data-test="logout-sidebar-link"]'
    INVENTORY_ITEM_LINK = '[data-test="inventory-item-name"]'

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

    def add_item_to_cart(self, item_slug: str):
        self.page.click(f'[data-test="add-to-cart-{item_slug}"]')

    def remove_backpack_from_cart(self):
        self.page.click(self.BACKPACK_REMOVE_BUTTON)

    def select_sort(self, value: str):
        self.page.select_option(self.SORT_DROPDOWN, value)

    def get_item_names(self) -> list[str]:
        return [name.strip() for name in self.page.locator(self.INVENTORY_ITEM_NAMES).all_inner_texts()]

    def get_item_prices(self) -> list[float]:
        prices = self.page.locator(self.INVENTORY_ITEM_PRICES).all_inner_texts()
        return [float(price.replace("$", "")) for price in prices]

    def get_cart_badge_count(self) -> int:
        badge = self.page.locator(self.CART_BADGE)
        if badge.count() == 0 or not badge.is_visible():
            return 0
        return int(badge.inner_text().strip())

    def open_cart(self):
        self.page.click(self.CART_LINK)

    def open_menu(self):
        self.page.click(self.MENU_BUTTON)

    def close_menu(self):
        self.page.click(self.MENU_CLOSE_BUTTON)

    def is_menu_open(self):
        expect(self.page.locator(self.MENU_WRAPPER)).to_have_attribute("aria-hidden", "false")

    def is_menu_closed(self):
        expect(self.page.locator(self.MENU_WRAPPER)).to_have_attribute("aria-hidden", "true")

    def click_product_by_name(self, product_name: str):
        self.page.locator(self.INVENTORY_ITEM_LINK).filter(has_text=product_name).click()

    def logout(self):
        self.open_menu()
        expect(self.page.locator(self.LOGOUT_LINK)).to_be_visible()
        self.page.click(self.LOGOUT_LINK)