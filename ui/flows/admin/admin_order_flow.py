"""
Admin Order Flow - 后台发货业务流程
职责：组合后台页面对象，实现完整的后台发货流程
"""

import random
from playwright.sync_api import Page

from ui.pages.admin.admin_order_page import AdminOrderPage


class AdminOrderFlow:
    """后台发货业务流程"""

    def __init__(self, admin_page: Page):
        self.admin_page = admin_page
        self.admin_order = AdminOrderPage(admin_page)

    def admin_ship_order(self, order_no: str, delivery_company: str = "顺丰", delivery_prefix: str = "SF"):
        """后台按订单编号搜索并发货

        Args:
            order_no: 订单编号
            delivery_company: 快递公司名称
            delivery_prefix: 物流单号前缀（2位拼音缩写）
        """
        self.admin_order.goto()
        self.admin_order.search_by_order_no(order_no)
        self.admin_order.click_ship()
        self.admin_order.select_delivery(delivery_company)
        tracking_no = f"{delivery_prefix}{random.randint(1000000000, 9999999999)}"
        self.admin_order.fill_tracking_no(tracking_no)
        self.admin_order.confirm_ship()
