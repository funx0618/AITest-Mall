"""
App Cart Page Object
页面：http://localhost:8060/#/pages/cart/cart
职责：购物车页面元素定位和基础交互
"""

from playwright.sync_api import Page, expect
from config.settings import WEB_BASE_URL


class AppCartPage:
    """App 购物车页面对象"""

    URL = WEB_BASE_URL + "/#/pages/cart/cart"

    def __init__(self, page: Page):
        self.page = page

        # ========== 购物车信息 ==========
        self.page_title = page.locator("text=购物车").first
        self.cart_items = page.locator('[class*="cart"] [class*="item"], [class*="goods-item"]')
        self.total_price = page.locator('[class*="total"], [class*="price"]').last
        self.empty_text = page.locator("text=购物车是空的")

        # ========== 操作按钮 ==========
        self.checkout_btn = page.get_by_text("去结算")
        self.clear_btn = page.get_by_text("清空")

        # ========== 底部导航 ==========
        self.nav_cart = page.get_by_text("购物车", exact=True)

    # ========== 页面导航 ==========
    def goto(self):
        """导航到购物车页面"""
        self.page.goto(self.URL)
        expect(self.page_title).to_be_visible(timeout=10000)
        return self

    # ========== 购物车操作 ==========
    def go_checkout(self):
        """点击去结算"""
        self.checkout_btn.click()
        return self
