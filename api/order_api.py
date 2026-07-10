"""
Order API - 订单相关接口封装
职责：通过 HTTP 请求操作订单数据
"""

import requests
from config.settings import WEB_USERNAME, WEB_PASSWORD


class OrderApi:
    """订单 API 封装"""

    BASE_URL = "http://localhost:8085"

    def __init__(self):
        self._token = None

    def _login(self) -> str:
        """通过 SSO 登录接口获取 token"""
        resp = requests.post(
            f"{self.BASE_URL}/sso/login",
            data={"username": WEB_USERNAME, "password": WEB_PASSWORD},
        )
        assert resp.status_code == 200, f"登录请求失败: {resp.status_code}"
        body = resp.json()
        assert body.get("code") == 200, f"登录失败: {body}"
        data = body.get("data", {})
        token_head = data.get("tokenHead", "")
        token = data.get("token", "")
        assert token, f"登录未返回token: {body}"
        return f"{token_head}{token}"

    def _get_auth_header(self) -> dict:
        """构造请求头，首次调用时自动登录获取token"""
        if not self._token:
            self._token = self._login()
        if self._token.lower().startswith("bearer "):
            return {"Authorization": self._token}
        return {"Authorization": f"Bearer {self._token}"}

    def get_latest_order(self, status: int = 1) -> dict:
        """获取最新订单（按createTime倒序取第一条）"""
        headers = self._get_auth_header()
        resp = requests.get(
            f"{self.BASE_URL}/order/list",
            params={"pageNum": 1, "pageSize": 10, "status": status},
            headers=headers,
        )
        assert resp.status_code == 200, f"API请求失败: {resp.status_code}"
        body = resp.json()
        assert body.get("code") == 200, f"API业务错误: {body}"
        orders = body.get("data", {}).get("list", [])
        assert orders, f"API未返回订单列表: {body}"
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
