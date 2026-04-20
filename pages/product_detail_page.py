from playwright.sync_api import Page, expect


class ProductDetailPage:
    DETAIL_CONTAINER = '[data-test="inventory-item-name"]'
    ITEM_NAME = '[data-test="inventory-item-name"]'
    ITEM_DESCRIPTION = '[data-test="inventory-item-desc"]'
    ITEM_PRICE = '[data-test="inventory-item-price"]'
    BACK_BUTTON = '[data-test="back-to-products"]'

    def __init__(self, page: Page):
        self.page = page

    def is_loaded(self):
        expect(self.page.locator(self.DETAIL_CONTAINER)).to_be_visible()
        expect(self.page.locator(self.ITEM_NAME)).to_be_visible()
        expect(self.page.locator(self.ITEM_PRICE)).to_be_visible()

    def get_product_name(self) -> str:
        return self.page.locator(self.ITEM_NAME).inner_text().strip()

    def go_back_to_products(self):
        self.page.click(self.BACK_BUTTON)
