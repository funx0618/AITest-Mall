"""
Admin Login Service - 后台管理登录接口封装
职责：封装登录相关的 API 请求，返回 ApiResponse
"""

from playwright.sync_api import APIRequestContext
from api.clients.api_response import ApiResponse
from api.clients.api_client import ApiClient
from config.settings import ADMIN_API_BASE_URL


class LoginService:
    """后台管理登录接口服务"""

    LOGIN_PATH = "/admin/login"

    def __init__(self, api_context: APIRequestContext):
        self._client = ApiClient(api_context, token="", base_url=ADMIN_API_BASE_URL)

    def login(self, username: str, password: str) -> ApiResponse:
        """发送登录请求"""
        resp = self._client.post(
            self.LOGIN_PATH,
            json_data={"username": username, "password": password},
        )
        return resp
