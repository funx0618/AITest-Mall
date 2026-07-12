"""
App Login Service - 前台商城登录接口封装
职责：封装前台登录相关的 API 请求，返回 ApiResponse
复用 admin 的 ApiResponse，直接使用 api_context 发送请求（登录接口不需要 Authorization 头）
"""

from playwright.sync_api import APIRequestContext
from api.clients.api_response import ApiResponse, build_api_response
from utils.logger import logger
from config.settings import APP_API_BASE_URL


class AppLoginService:
    """前台商城登录接口服务"""

    LOGIN_PATH = "/sso/login"

    def __init__(self, api_context: APIRequestContext):
        self._api_context = api_context
        self._base_url = APP_API_BASE_URL

    def login(self, username: str, password: str) -> ApiResponse:
        """发送登录请求（不带 Authorization 头，使用 form 表单）"""
        url = f"{self._base_url}{self.LOGIN_PATH}"
        logger.info(f"POST {url}")
        resp = self._api_context.post(
            url,
            form={"username": username, "password": password},
        )
        return build_api_response(resp, f"POST {self.LOGIN_PATH}")
