"""
App Order Flow - Web App 端下单业务流程
职责：组合 Web App 页面对象，实现完整的下单 → 查看订单 → 确认收货流程
"""

import re
from playwright.sync_api import Page, expect

from ui.pages.app.app_login_page import AppLoginPage
from ui.pages.app.app_home_page import AppHomePage
from ui.pages.app.app_product_page import AppProductPage
from ui.pages.app.app_cart_page import AppCartPage
from ui.pages.app.app_checkout_page import AppCheckoutPage
from ui.pages.app.app_order_page import AppMyOrderPage


class AppOrderFlow:
    """Web App 端下单业务流程"""

    def __init__(self, web_page: Page):
        self.web_page = web_page
        self.login_page = AppLoginPage(web_page)
        self.home_page = AppHomePage(web_page)
        self.product_page = AppProductPage(web_page)
        self.cart_page = AppCartPage(web_page)
        self.checkout_page = AppCheckoutPage(web_page)
        self.order_page = AppMyOrderPage(web_page)

    # ========== Step 1: Web App 登录 ==========
    def do_web_login(self, username: str, password: str):
        """Web App 用户登录"""
        self.login_page.goto()
        self.login_page.login(username, password)
        expect(self.web_page).to_have_url(re.compile(r".*#/$"), timeout=15000)

    # ========== Step 2: 搜索并加入购物车 ==========
    def search_and_add_to_cart(self, keyword: str, product_name: str):
        """搜索商品并加入购物车"""
        self.home_page.search(keyword)
        self.home_page.click_product_by_name(product_name)
        self.product_page.add_to_cart()

    # ========== Step 3: 购物车结算 ==========
    def go_checkout(self):
        """进入购物车并去结算"""
        self.cart_page.goto()
        self.cart_page.go_checkout()

    # ========== Step 4: 提交订单 ==========
    def submit_order(self):
        """提交订单"""
        self.checkout_page.submit_order()

    # ========== Step 5: 选择支付方式并支付 ==========
    def pay_with_wechat(self):
        """选择微信支付并去支付"""
        self.checkout_page.select_wechat_pay()
        self.checkout_page.go_pay()

    # ========== Step 6: 查看订单，获取订单编号 ==========
    def get_order_no_from_detail(self) -> str:
        """进入订单详情获取订单编号"""
        self.order_page.goto_orders()
        self.order_page.click_tab("待发货")
        self.order_page.click_first_order()
        return self.order_page.get_order_no()

    # ========== Step 9: Web App 确认收货 ==========
    def confirm_receipt_in_web(self):
        """在 Web App 确认收货"""
        self.order_page.goto_orders()
        self.order_page.click_tab("待收货")
        self.order_page.click_first_order()
        self.order_page.confirm_receipt()
