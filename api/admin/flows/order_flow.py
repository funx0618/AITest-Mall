"""
Admin Order Flow - 后台管理订单业务流程封装
职责：封装后台管理订单相关的业务操作流程
"""

from playwright.sync_api import APIRequestContext
from api.admin.services.order_service import AdminOrderService


class AdminOrderFlow:
    """后台管理订单业务流程"""

    def __init__(self, api_context: APIRequestContext, token: str):
        self.order_service = AdminOrderService(api_context, token)

    def get_latest_order_info(self, status: int = 1) -> tuple[int, str]:
        """获取最新订单信息，返回 (order_id, order_sn)"""
        return self.order_service.get_latest_order_sn(status)

    def get_latest_order_id(self, status: int = 1) -> int:
        """获取最新订单的orderId"""
        return self.order_service.get_latest_order_id(status)

    def get_latest_order_sn(self, status: int = 1) -> str:
        """获取最新订单的orderSn"""
        _, order_sn = self.order_service.get_latest_order_sn(status)
        return order_sn
