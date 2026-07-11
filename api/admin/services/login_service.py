"""
Admin Login Service - 后台管理登录接口封装
职责：封装登录相关的 API 请求，返回 ApiResponse
"""

from playwright.sync_api import APIRequestContext
from api.admin.clients.api_response import ApiResponse
from api.admin.clients.api_client import AdminApiClient


class LoginService:
    """后台管理登录接口服务"""

    LOGIN_PATH = "/admin/login"

    def __init__(self, api_context: APIRequestContext):
        self._client = AdminApiClient(api_context, token="")

    def login(self, username: str, password: str) -> ApiResponse:
        """发送登录请求"""
        resp = self._client.post(
            self.LOGIN_PATH,
            json_data={"username": username, "password": password},
        )
        return resp
