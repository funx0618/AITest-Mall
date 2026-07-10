"""
App Login Page Object
页面：http://localhost:8060/#/pages/public/login
职责：只负责页面元素定位和基础交互
"""

from playwright.sync_api import Page, expect
from config.settings import WEB_LOGIN_URL


class AppLoginPage:
    """App 登录页面对象"""

    URL = WEB_LOGIN_URL

    def __init__(self, page: Page):
        self.page = page

        # ========== 表单元素 ==========
        self.username_input = page.get_by_role("textbox").first
        self.password_input = page.get_by_role("textbox").nth(1)
        self.login_btn = page.get_by_text("登录", exact=True)

    # ========== 页面导航 ==========
    def goto(self):
        """导航到登录页面"""
        self.page.goto(self.URL)
        expect(self.login_btn).to_be_visible(timeout=10000)
        return self

    # ========== 登录操作 ==========
    def login(self, username: str, password: str):
        """执行登录操作"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_btn.click()
        return self
