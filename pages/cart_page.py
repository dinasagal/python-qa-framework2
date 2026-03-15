from playwright.sync_api import Page, expect


class CartPage:
    CART_CONTAINER = '[data-test="cart-list"]'
    CART_ITEMS = '[data-test="inventory-item"]'
    ITEM_NAMES = '[data-test="inventory-item-name"]'

    def __init__(self, page: Page):
        self.page = page

    def is_loaded(self):
        expect(self.page.locator(self.CART_CONTAINER)).to_be_visible()

    def has_item(self, item_name: str) -> bool:
        items = self.page.locator(self.ITEM_NAMES)
        count = items.count()

        for i in range(count):
            if items.nth(i).inner_text().strip() == item_name:
                return True
        return False

    def get_cart_count(self) -> int:
        return self.page.locator(self.CART_ITEMS).count()