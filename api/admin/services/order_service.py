"""
Admin Order Service - 后台管理订单相关接口封装
职责：通过 HTTP 请求操作后台管理订单数据
对应 Controller：OmsOrderController
Base path：/order
"""

from playwright.sync_api import APIRequestContext
from api.clients.api_client import ApiClient
from api.clients.api_response import ApiResponse
from config.settings import ADMIN_API_BASE_URL


class AdminOrderService(ApiClient):
    """后台管理订单 API 封装，对应 OmsOrderController"""

    def __init__(self, api_context: APIRequestContext, token: str):
        super().__init__(api_context, token, base_url=ADMIN_API_BASE_URL)

    # ==================== OmsOrderController ====================

    def get_order_list(self, page_num: int = 1, page_size: int = 10, **kwargs) -> ApiResponse:
        """分页查询订单列表
        GET /order/list
        可选参数：orderSn, status, receiverKeyword 等
        """
        params = {"pageNum": page_num, "pageSize": page_size, **kwargs}
        return self.get("/order/list", params=params)

    def get_order_detail(self, order_id: int) -> ApiResponse:
        """获取订单详情（订单信息、商品、日志）
        GET /order/{id}
        """
        return self.get(f"/order/{order_id}")

    def update_delivery(self, delivery_param: list[dict]) -> ApiResponse:
        """批量发货
        POST /order/update/delivery
        """
        return self.post("/order/update/delivery", json_data=delivery_param)

    def close_orders(self, ids: list[int]) -> ApiResponse:
        """批量关闭订单
        POST /order/update/close
        """
        return self.post("/order/update/close", json_data=ids)

    def delete_orders(self, ids: list[int]) -> ApiResponse:
        """批量删除订单
        POST /order/delete
        """
        return self.post("/order/delete", json_data=ids)

    def update_receiver_info(self, receiver_info: dict) -> ApiResponse:
        """修改收货人信息
        POST /order/update/receiverInfo
        """
        return self.post("/order/update/receiverInfo", json_data=receiver_info)

    def update_money_info(self, money_info: dict) -> ApiResponse:
        """修改订单费用信息
        POST /order/update/moneyInfo
        """
        return self.post("/order/update/moneyInfo", json_data=money_info)

    def update_note(self, id: int, note: str, note_type: int) -> ApiResponse:
        """修改订单备注
        POST /order/update/note
        note_type: 0=订单备注, 1=操作备注
        """
        return self.post("/order/update/note", json_data={"id": id, "note": note, "noteType": note_type})


