"""
App Order Service - 前台商城订单相关接口封装
职责：通过 HTTP 请求操作订单数据
对应 Controller：OmsPortalOrderController
Base path：/order
"""

import json
from playwright.sync_api import APIRequestContext
from api.clients.api_client import ApiClient
from api.clients.api_response import ApiResponse
from config.settings import APP_API_BASE_URL


class AppOrderService(ApiClient):
    """前台商城订单 API 封装，对应 OmsPortalOrderController"""

    def __init__(self, api_context: APIRequestContext, token: str):
        super().__init__(api_context, token, base_url=APP_API_BASE_URL)

    # ==================== OmsPortalOrderController ====================

    def generate_confirm_order(self, cart_ids: list[int]) -> ApiResponse:
        """生成确认单信息
        POST /order/generateConfirmOrder
        请求体：购物车 ID 数组 [1, 2, 3]
        """
        url = f"{self.BASE_URL}/order/generateConfirmOrder"
        resp = self._api_context.post(
            url,
            data=json.dumps(cart_ids),
            headers={**self._get_auth_header(), "Content-Type": "application/json"},
        )
        from api.clients.api_response import build_api_response
        return build_api_response(resp, "POST /order/generateConfirmOrder")

    def generate_order(self, order_param: dict) -> ApiResponse:
        """提交订单
        POST /order/generateOrder
        请求体：OrderParam
        """
        return self.post("/order/generateOrder", json_data=order_param)

    def get_order_list(self, status: int = -1, page_num: int = 1, page_size: int = 5) -> ApiResponse:
        """查询用户订单列表
        GET /order/list
        """
        params = {"status": status, "pageNum": page_num, "pageSize": page_size}
        return self.get("/order/list", params=params)

    def get_order_detail(self, order_id: int) -> ApiResponse:
        """获取订单详情
        GET /order/detail/{orderId}
        """
        return self.get(f"/order/detail/{order_id}")

    def cancel_user_order(self, order_id: int) -> ApiResponse:
        """用户取消订单
        POST /order/cancelUserOrder
        """
        url = f"{self.BASE_URL}/order/cancelUserOrder"
        resp = self._api_context.post(
            url,
            form={"orderId": order_id},
            headers=self._get_auth_header(),
        )
        from api.clients.api_response import build_api_response
        return build_api_response(resp, "POST /order/cancelUserOrder")

    def confirm_receive_order(self, order_id: int) -> ApiResponse:
        """用户确认收货
        POST /order/confirmReceiveOrder
        """
        url = f"{self.BASE_URL}/order/confirmReceiveOrder"
        resp = self._api_context.post(
            url,
            form={"orderId": order_id},
            headers=self._get_auth_header(),
        )
        from api.clients.api_response import build_api_response
        return build_api_response(resp, "POST /order/confirmReceiveOrder")

    def delete_order(self, order_id: int) -> ApiResponse:
        """用户删除订单
        POST /order/deleteOrder
        """
        url = f"{self.BASE_URL}/order/deleteOrder"
        resp = self._api_context.post(
            url,
            form={"orderId": order_id},
            headers=self._get_auth_header(),
        )
        from api.clients.api_response import build_api_response
        return build_api_response(resp, "POST /order/deleteOrder")

    def pay_success(self, order_id: int, pay_type: int) -> ApiResponse:
        """模拟支付成功回调
        POST /order/paySuccess
        参数：orderId, payType
        """
        url = f"{self.BASE_URL}/order/paySuccess"
        resp = self._api_context.post(
            url,
            form={"orderId": order_id, "payType": pay_type},
            headers=self._get_auth_header(),
        )
        from api.clients.api_response import build_api_response
        return build_api_response(resp, "POST /order/paySuccess")
