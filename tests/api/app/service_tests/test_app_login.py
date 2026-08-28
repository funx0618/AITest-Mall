"""
App Login API 测试用例
职责：验证前台商城登录接口的各种场景
"""

import pytest
from playwright.sync_api import Playwright
from config.settings import APP_API_BASE_URL, WEB_USERNAME, WEB_PASSWORD
from api.app.services.login import AppLoginService


@pytest.fixture
def api_context(playwright: Playwright):
    """无认证的 API 请求上下文（用于测试登录接口本身）"""
    ctx = playwright.request.new_context(base_url=APP_API_BASE_URL)
    yield ctx
    ctx.dispose()


class TestAppLogin:
    """前台商城登录接口测试"""

    def test_login_with_wrong_password(self, api_context):
        """输入正确的用户名和错误的密码，应返回用户名或密码错误"""
        service = AppLoginService(api_context)
        resp = service.login(WEB_USERNAME, "wrong_password")
        assert resp.code == 404, f"错误密码应返回code=404，实际: {resp.json}"
        assert "用户名或密码错误" in resp.message, f"错误提示不匹配: {resp.message}"

    def test_login_with_wrong_username(self, api_context):
        """输入错误的用户名和正确的密码，应返回用户名或密码错误"""
        service = AppLoginService(api_context)
        resp = service.login("wrong_user", WEB_PASSWORD)
        assert resp.code == 404, f"错误用户名应返回code=404，实际: {resp.json}"
        assert "用户名或密码错误" in resp.message, f"错误提示不匹配: {resp.message}"
