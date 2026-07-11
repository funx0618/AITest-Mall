"""
Admin API Client - 后台管理 HTTP 客户端基类
职责：封装 HTTP 请求发送和响应获取，不做业务断言
使用 Playwright APIRequestContext 实现
"""

from playwright.sync_api import APIRequestContext
from api.api_response import ApiResponse
from utils.logger import logger
from config.settings import ADMIN_API_BASE_URL


class AdminApiClient:
    """后台管理 API 客户端，仅负责发送请求和返回 ApiResponse"""

    BASE_URL = ADMIN_API_BASE_URL

    def __init__(self, api_context: APIRequestContext, token: str, base_url: str | None = None):
        if base_url:
            self.BASE_URL = base_url
        self._api_context = api_context
        self._token = token

    def _get_auth_header(self) -> dict:
        """构造请求头"""
        if self._token.lower().startswith("bearer "):
            return {"Authorization": self._token}
        return {"Authorization": f"Bearer {self._token}"}

    def _build_response(self, resp, action: str) -> ApiResponse:
        """将 Playwright Response 转换为 ApiResponse 并记录日志"""
        body = resp.json()
        api_resp = ApiResponse(
            status_code=resp.status,
            json_data=body,
            text=resp.text(),
        )
        logger.info(f"{action} | status={resp.status}, code={api_resp.code}")
        return api_resp

    def get(self, path: str, params: dict | None = None) -> ApiResponse:
        """发送 GET 请求"""
        url = f"{self.BASE_URL}{path}"
        logger.info(f"GET {url} params={params}")
        resp = self._api_context.get(url, params=params, headers=self._get_auth_header())
        return self._build_response(resp, f"GET {path}")

    def post(self, path: str, data: dict | None = None, json_data: dict | None = None) -> ApiResponse:
        """发送 POST 请求"""
        url = f"{self.BASE_URL}{path}"
        logger.info(f"POST {url} data={data}, json={json_data}")
        kwargs: dict = {"headers": self._get_auth_header()}
        if data:
            kwargs["form"] = data
        if json_data:
            kwargs["data"] = json_data
        resp = self._api_context.post(url, **kwargs)
        return self._build_response(resp, f"POST {path}")

    def put(self, path: str, json_data: dict | None = None) -> ApiResponse:
        """发送 PUT 请求"""
        url = f"{self.BASE_URL}{path}"
        logger.info(f"PUT {url} json={json_data}")
        resp = self._api_context.put(url, data=json_data, headers=self._get_auth_header())
        return self._build_response(resp, f"PUT {path}")

    def delete(self, path: str, params: dict | None = None) -> ApiResponse:
        """发送 DELETE 请求"""
        url = f"{self.BASE_URL}{path}"
        logger.info(f"DELETE {url} params={params}")
        resp = self._api_context.delete(url, params=params, headers=self._get_auth_header())
        return self._build_response(resp, f"DELETE {path}")
