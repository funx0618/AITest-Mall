"""
App Address Service - 前台商城收货地址相关接口封装
职责：通过 HTTP 请求操作收货地址数据
对应 Controller：UmsMemberReceiveAddressController
Base path：/member/address
"""

from playwright.sync_api import APIRequestContext
from api.clients.api_client import ApiClient
from api.clients.api_response import ApiResponse
from config.settings import APP_API_BASE_URL


class AppAddressService(ApiClient):
    """前台商城收货地址 API 封装，对应 UmsMemberReceiveAddressController"""

    def __init__(self, api_context: APIRequestContext, token: str):
        super().__init__(api_context, token, base_url=APP_API_BASE_URL)

    # ==================== UmsMemberReceiveAddressController ====================

    def add_address(self, address: dict) -> ApiResponse:
        """添加收货地址
        POST /member/address/add
        请求体：UmsMemberReceiveAddress
        """
        return self.post("/member/address/add", json_data=address)

    def delete_address(self, address_id: int) -> ApiResponse:
        """删除收货地址
        POST /member/address/delete/{id}
        """
        return self.post(f"/member/address/delete/{address_id}")

    def update_address(self, address_id: int, address: dict) -> ApiResponse:
        """修改收货地址
        POST /member/address/update/{id}
        """
        return self.post(f"/member/address/update/{address_id}", json_data=address)

    def list_address(self) -> ApiResponse:
        """获取所有收货地址
        GET /member/address/list
        """
        return self.get("/member/address/list")

    def get_address_detail(self, address_id: int) -> ApiResponse:
        """获取收货地址详情
        GET /member/address/{id}
        """
        return self.get(f"/member/address/{address_id}")
