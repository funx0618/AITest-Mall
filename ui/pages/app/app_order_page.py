"""
App My Order Page Object
页面：我的订单页面
职责：订单列表、订单详情的元素定位和基础交互
"""

import re
from datetime import datetime
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
        self.order_items = page.locator(".order-item")

        # ========== 订单详情页 ==========
        self.order_no = page.locator('[class*="order-no"], [class*="orderNo"], text=/\\d{15,}/')
        self.confirm_receipt_btn = page.get_by_text("确认收货")
        self.waiting_delivery = page.locator("text=等待发货")
        self.waiting_receipt = page.locator("text=待收货")
        self.detail_status = page.locator('[class*="status"], [class*="order-status"]')

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

    # ========== 订单查找与详情 ==========

    def find_latest_order_by_product(self, product_name: str):
        """在全部订单列表中，按商品名称查找并返回最新的订单

        Args:
            product_name: 商品名称

        Returns:
            匹配的最新订单 Locator
        """
        expect(self.order_items.first).to_be_visible(timeout=10000)
        orders = self.order_items
        matched_orders = []

        for i in range(orders.count()):
            order = orders.nth(i)
            title = order.locator(".title.clamp")
            if title.inner_text().strip() == product_name:
                matched_orders.append(order)

        assert matched_orders, f"未找到商品「{product_name}」对应的订单"

        # 按订单时间倒序，获取最新订单
        latest_order = max(
            matched_orders,
            key=lambda o: datetime.strptime(
                o.locator(".time").inner_text().strip(),
                "%Y-%m-%d %H:%M:%S"
            )
        )
        return latest_order

    def verify_order_status(self, order_locator, expected_status: str):
        """验证订单列表中某个订单包含指定状态文本

        Args:
            order_locator: 订单元素 Locator
            expected_status: 期望的状态文本，如 "等待发货"
        """
        expect(order_locator).to_contain_text(expected_status, timeout=5000)
        return self

    def click_order_to_detail(self, order_locator):
        """点击订单进入详情页"""
        order_locator.click()
        expect(self.page.get_by_text("订单详情")).to_be_visible(timeout=10000)
        return self

    def get_order_no_from_detail(self) -> str:
        """从订单详情页获取订单编号"""
        order_no_row = self.page.locator(".yt-list-cell").filter(
            has_text="订单编号"
        )
        expect(order_no_row).to_be_visible(timeout=10000)
        order_no = order_no_row.locator(".cell-tip")
        order_no_text = order_no.inner_text()
        return order_no_text.strip()

    def get_submit_time_from_detail(self) -> str:
        """从订单详情页获取提交时间，格式 %Y-%m-%d %H:%M:%S"""
        time_row = self.page.locator(".yt-list-cell").filter(
            has_text="提交时间"
        )
        expect(time_row).to_be_visible(timeout=10000)
        return time_row.locator(".cell-tip").inner_text().strip()

    def find_order_by_time_and_product(self, time_str: str, product_name: str):
        """在当前 tab 的订单列表中，按创建时间和商品名称定位订单

        Args:
            time_str: 订单创建时间，如 "2026-08-25 16:48:29"
            product_name: 商品名称

        Returns:
            匹配的订单 Locator
        """
        expect(self.order_items.first).to_be_visible(timeout=10000)
        for i in range(self.order_items.count()):
            order = self.order_items.nth(i)
            time_text = order.locator(".time").inner_text().strip()
            title_text = order.locator(".title.clamp").inner_text().strip()
            if time_text == time_str and title_text == product_name:
                return order
        assert False, f"未找到创建时间={time_str}、商品={product_name} 的订单"
