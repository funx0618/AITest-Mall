"""
API Client - HTTP 客户端基类
职责：封装 HTTP 请求发送和响应获取，不做业务断言
使用 Playwright APIRequestContext 实现
"""

import json
from playwright.sync_api import APIRequestContext
from api.clients.api_response import ApiResponse, build_api_response
from utils.logger import logger


class ApiClient:
    """通用 API 客户端，仅负责发送请求和返回 ApiResponse"""

    def __init__(self, api_context: APIRequestContext, token: str, base_url: str):
        self.BASE_URL = base_url
        self._api_context = api_context
        self._token = token

    def _get_auth_header(self) -> dict:
        """构造请求头"""
        if self._token.lower().startswith("bearer "):
            return {"Authorization": self._token}
        return {"Authorization": f"Bearer {self._token}"}

    def get(self, path: str, params: dict | None = None) -> ApiResponse:
        """发送 GET 请求"""
        url = f"{self.BASE_URL}{path}"
        logger.info(f"GET {url} params={params}")
        resp = self._api_context.get(url, params=params, headers=self._get_auth_header())
        return build_api_response(resp, f"GET {path}")

    def post(self, path: str, data: dict | None = None, json_data: dict | None = None) -> ApiResponse:
        """发送 POST 请求"""
        url = f"{self.BASE_URL}{path}"
        logger.info(f"POST {url}")
        kwargs = {"headers": self._get_auth_header()}
        if json_data is not None:
            kwargs["data"] = json.dumps(json_data)
            kwargs["headers"]["Content-Type"] = "application/json"
        elif data is not None:
            kwargs["form"] = data
        resp = self._api_context.post(url, **kwargs)
        return build_api_response(resp, f"POST {path}")

    def put(self, path: str, json_data: dict | None = None) -> ApiResponse:
        """发送 PUT 请求"""
        url = f"{self.BASE_URL}{path}"
        logger.info(f"PUT {url}")
        resp = self._api_context.put(url, json_data=json_data, headers=self._get_auth_header())
        return build_api_response(resp, f"PUT {path}")

    def delete(self, path: str) -> ApiResponse:
        """发送 DELETE 请求"""
        url = f"{self.BASE_URL}{path}"
        logger.info(f"DELETE {url}")
        resp = self._api_context.delete(url, headers=self._get_auth_header())
        return build_api_response(resp, f"DELETE {path}")
