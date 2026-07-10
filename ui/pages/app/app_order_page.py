"""
App My Order Page Object
页面：我的订单页面
职责：订单列表、订单详情的元素定位和基础交互
"""

import re
from playwright.sync_api import Page, expect
from config.settings import WEB_BASE_URL


class AppMyOrderPage:
    """App 我的订单页面对象"""

    ORDERS_URL = WEB_BASE_URL + "/#/pages/order/list"

    def __init__(self, page: Page):
        self.page = page

        # ========== 订单列表页 ==========
        self.tab_all = page.get_by_text("全部", exact=True)
        self.tab_pending_receipt = page.get_by_text("待收货", exact=True)
        self.tab_completed = page.get_by_text("已完成", exact=True)

        # ========== 订单详情页 ==========
        self.order_no = page.locator('[class*="order-no"], [class*="orderNo"], text=/\\d{15,}/')
        self.confirm_receipt_btn = page.get_by_text("确认收货")
        self.waiting_delivery = page.locator("text=等待发货")
        self.waiting_receipt = page.locator("text=待收货")

        # ========== 底部导航 ==========
        self.nav_my = page.get_by_text("我的", exact=True)

    # ========== 页面导航 ==========
    def goto_orders(self):
        """导航到全部订单页面"""
        self.page.goto(self.ORDERS_URL)
        return self

    # ========== 订单操作 ==========
    def go_to_my_page(self):
        """从底部导航进入我的页面"""
        self.nav_my.click()
        return self

    def click_tab(self, tab_name: str):
        """点击订单状态 Tab"""
        tab = self.page.get_by_text(tab_name, exact=True)
        expect(tab).to_be_visible(timeout=10000)
        tab.click()
        return self

    def goto_order_detail(self, order_id: int):
        """导航到订单详情页"""
        self.page.goto(
            f"{WEB_BASE_URL}/#/pages/order/orderDetail?orderId={order_id}"
        )
        self.page.wait_for_url(
            re.compile(rf"orderId={order_id}"), timeout=10000
        )
        return self

    def confirm_receipt(self):
        """确认收货，点击后在弹窗中再次确认"""
        self.confirm_receipt_btn.click()
        # uni-app showModal 弹窗不用 button 标签，等待弹窗文本出现
        self.page.get_by_text("是否要确认收货").wait_for(timeout=5000)
        # 点击弹窗中的"确定"文本（可能是 div/span 而非 button）
        self.page.get_by_text("确定", exact=True).last.click()
        return self
