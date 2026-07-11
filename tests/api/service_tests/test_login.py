"""
Login API 测试用例
职责：验证 SSO 登录接口的各种场景
"""

from playwright.sync_api import Playwright
from config.settings import ADMIN_API_BASE_URL, DEFAULT_USERNAME, DEFAULT_PASSWORD
from api.admin.services.login_service import LoginService


class TestLogin:
    """SSO 登录接口测试"""

    def test_login_with_wrong_password(self, playwright: Playwright):
        """输入正确的用户名和错误的密码，登录应失败"""
        api_context = playwright.request.new_context(base_url=ADMIN_API_BASE_URL)
        try:
            service = LoginService(api_context)
            resp = service.login(DEFAULT_USERNAME, "wrong_password")
            assert resp.code != 200, f"错误密码不应登录成功: {resp.json}"
        finally:
            api_context.dispose()

    def test_login_with_wrong_username(self, playwright: Playwright):
        """输入错误的用户名和正确的密码，登录应失败"""
        api_context = playwright.request.new_context(base_url=ADMIN_API_BASE_URL)
        try:
            service = LoginService(api_context)
            resp = service.login("wrong_user", DEFAULT_PASSWORD)
            assert resp.code != 200, f"错误用户名不应登录成功: {resp.json}"
        finally:
            api_context.dispose()

    def test_login_success(self, playwright: Playwright):
        """输入正确的用户名和密码，登录应成功并返回 token"""
        api_context = playwright.request.new_context(base_url=ADMIN_API_BASE_URL)
        try:
            service = LoginService(api_context)
            resp = service.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
            assert resp.ok, f"登录请求失败: HTTP {resp.status_code}"
            assert resp.code == 200, f"登录失败: {resp.json}"

            data = resp.data
            token = data.get("token", "")
            token_head = data.get("tokenHead", "")
            assert token, f"登录未返回token: {resp.json}"
            assert token_head, f"登录未返回tokenHead: {resp.json}"
        finally:
            api_context.dispose()
