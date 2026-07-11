"""
Login API 测试用例
职责：验证 SSO 登录接口的各种场景
"""

import pytest
from playwright.sync_api import Playwright
from config.settings import ADMIN_API_BASE_URL, DEFAULT_USERNAME, DEFAULT_PASSWORD
from api.admin.services.login_service import LoginService


@pytest.fixture
def api_context(playwright: Playwright):
    """无认证的 API 请求上下文（用于测试登录接口本身）"""
    ctx = playwright.request.new_context(base_url=ADMIN_API_BASE_URL)
    yield ctx
    ctx.dispose()


class TestLogin:
    """SSO 登录接口测试"""

    def test_login_with_wrong_password(self, api_context):
        """输入正确的用户名和错误的密码，登录应失败"""
        service = LoginService(api_context)
        resp = service.login(DEFAULT_USERNAME, "wrong_password")
        assert resp.code != 200, f"错误密码不应登录成功: {resp.json}"

    def test_login_with_wrong_username(self, api_context):
        """输入错误的用户名和正确的密码，登录应失败"""
        service = LoginService(api_context)
        resp = service.login("wrong_user", DEFAULT_PASSWORD)
        assert resp.code != 200, f"错误用户名不应登录成功: {resp.json}"

    def test_login_success(self, api_context):
        """输入正确的用户名和密码，登录应成功并返回 token"""
        service = LoginService(api_context)
        resp = service.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        assert resp.ok, f"登录请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"登录失败: {resp.json}"

        data = resp.data
        token = data.get("token", "")
        token_head = data.get("tokenHead", "")
        assert token, f"登录未返回token: {resp.json}"
        assert token_head, f"登录未返回tokenHead: {resp.json}"
