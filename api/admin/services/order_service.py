"""
Admin Order Service - 后台管理订单相关接口封装
职责：通过 HTTP 请求操作后台管理订单数据，负责业务断言
"""

from playwright.sync_api import APIRequestContext
from api.admin.clients.admin_api_client import AdminApiClient
from api.api_response import ApiResponse


class AdminOrderService(AdminApiClient):
    """后台管理订单 API 封装，继承 AdminApiClient 并添加业务断言"""

    def __init__(self, api_context: APIRequestContext, token: str):
        super().__init__(api_context, token)

    def get_latest_order(self, status: int = 1) -> dict:
        """获取最新订单（按createTime倒序取第一条）"""
        resp = self.get("/order/list", params={"pageNum": 1, "pageSize": 10, "status": status})
        assert resp.ok, f"API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"API业务错误: {resp.json}"
        orders = resp.data.get("list", [])
        assert orders, f"API未返回订单列表: {resp.json}"
        orders.sort(key=lambda o: o.get("createTime", ""), reverse=True)
        return orders[0]

    def get_latest_order_sn(self, status: int = 1) -> tuple[int, str]:
        """获取最新订单的orderId和orderSn，返回 (order_id, order_sn)"""
        order = self.get_latest_order(status)
        order_sn = order.get("orderSn", "")
        order_id = order.get("id")
        assert order_sn, f"未能获取到orderSn, 首条订单: {order}"
        assert order_id, f"未能获取到orderId, 首条订单: {order}"
        return order_id, order_sn

    def get_latest_order_id(self, status: int = 1) -> int:
        """获取最新订单的orderId"""
        order = self.get_latest_order(status)
        order_id = order.get("id")
        assert order_id, f"未能获取到orderId, 首条订单: {order}"
        return order_id
