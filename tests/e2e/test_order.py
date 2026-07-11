"""
端到端下单测试用例
测试目标：完成完整的下单 → 发货 → 收货流程
涉及页面：
  - Web App: http://localhost:8060
  - Admin:   http://localhost:8090
"""

import re
import random
import pytest
from playwright.sync_api import Page, expect
from ui.pages.app.app_home_page import AppHomePage
from ui.pages.app.app_product_page import AppProductPage
from ui.pages.app.app_cart_page import AppCartPage
from ui.pages.app.app_checkout_page import AppCheckoutPage
from ui.pages.app.app_order_page import AppMyOrderPage
from ui.pages.admin.admin_order_page import AdminOrderPage
from api.order_api import OrderApi
from utils.data_loader import load_yaml

# 加载测试数据
test_data = load_yaml("e2e/test_order.yaml")


class TestNormalOrder:
    """普通下单流程测试（无优惠券、无积分抵扣）"""

    def test_normal_order_flow(self, app_logged_in: Page, admin_logged_in_page: Page):
        """完整下单流程：搜索商品 → 加入购物车 → 结算 → 支付 → 后台发货 → 确认收货"""
        data = test_data["test_normal_order"]
        keyword = data["keyword"]
        product_name = data["product_name"]

        web_page = app_logged_in
        admin_page = admin_logged_in_page

        # ===== Step 1-2: 搜索商品并加入购物车 =====
        home = AppHomePage(web_page)
        home.search(keyword)
        home.click_product_by_name(product_name)

        product = AppProductPage(web_page)
        product.add_to_cart()

        # ===== Step 3: 进入购物车，点击去结算 =====
        cart = AppCartPage(web_page)
        cart.goto()
        cart.go_checkout()

        # ===== Step 3.5: 选择默认收货地址 =====
        checkout = AppCheckoutPage(web_page)
        checkout.select_default_address()

        # ===== Step 4: 提交订单，并在弹窗中点击去支付 =====
        checkout.submit_order()

        # ===== Step 5: 在支付页选择微信支付并完成支付 =====
        checkout.select_wechat_pay()
        checkout.go_pay()

        # ===== Step 6: 通过API获取最新订单编号 =====
        order_api = OrderApi()
        order_id, order_no = order_api.get_latest_order_sn()

        # ===== Step 7-8: 后台按订单编号查询并发货 =====
        delivery_company = data["delivery_company"]
        delivery_prefix = data["delivery_prefix"]
        admin_order = AdminOrderPage(admin_page)
        admin_order.goto()
        admin_order.search_by_order_no(order_no)
        admin_order.click_ship()
        admin_order.select_delivery(delivery_company)
        tracking_no = f"{delivery_prefix}{random.randint(1000000000, 9999999999)}"
        admin_order.fill_tracking_no(tracking_no)
        admin_order.confirm_ship()

        # ===== Step 9: Web App 进入订单详情，验证待收货 =====
        order_page = AppMyOrderPage(web_page)
        order_page.goto_order_detail(order_id)
        expect(web_page.locator("text=待收货").first).to_be_visible(timeout=10000)

        # ===== Step 10: 确认收货，验证订单进入已完成 =====
        order_page.confirm_receipt()
        expect(web_page.locator("text=交易完成").first).to_be_visible(timeout=10000)
