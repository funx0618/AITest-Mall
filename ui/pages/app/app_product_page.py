"""
App Product Detail Page Object
页面：http://localhost:8060/#/pages/product/product?id=xxx
职责：商品详情页元素定位和基础交互
"""

from playwright.sync_api import Page, expect


class AppProductPage:
    """App 商品详情页对象"""

    def __init__(self, page: Page):
        self.page = page

        # ========== 商品信息 ==========
        self.product_title = page.locator('[class*="product"] [class*="name"], [class*="goods"] [class*="name"]').first
        self.product_price = page.locator('[class*="price"]').first

        # ========== SKU 弹窗 ==========
        self.sku_popup = page.locator('[class*="sku"], [class*="popup--bottom"], .van-popup--bottom')
        self.sku_options = page.locator('[class*="sku"] [class*="item"], [class*="popup"] [class*="tag"]')

        # ========== 操作按钮 ==========
        self.add_cart_btn = page.get_by_text("加入购物车")
        self.buy_now_btn = page.get_by_text("立即购买")
        self.confirm_btn = page.get_by_text("确定")

        # ========== 提示信息 ==========
        self.success_message = page.locator("text=操作成功")
        self.login_prompt = page.locator("text=你还没登录")

    # ========== 商品操作 ==========
    def add_to_cart(self):
        """点击加入购物车，在 SKU 弹窗中确认"""
        self.add_cart_btn.click()
        # 如果出现 SKU 弹窗，点击确定
        if self.confirm_btn.is_visible():
            self.confirm_btn.click()
        # 等待添加成功提示
        expect(self.success_message).to_be_visible(timeout=5000)
        return self

    def buy_now(self):
        """点击立即购买"""
        self.buy_now_btn.click()
        return self
