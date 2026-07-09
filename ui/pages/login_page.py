"""
Login Page Object
页面：http://localhost:8090/#/login
职责：只负责页面元素定位和基础交互
"""

from playwright.sync_api import Page, expect
from config.settings import LOGIN_URL


class LoginPage:
    """登录页面对象"""

    URL = LOGIN_URL

    def __init__(self, page: Page):
        self.page = page

        # ========== 表单元素 ==========
        self.username_input = page.get_by_placeholder("请输入用户名")
        self.password_input = page.get_by_placeholder("请输入密码")
        self.login_btn = page.get_by_role("button", name="登录")
        self.eye_icon = page.locator('[placeholder="请输入密码"] ~ .el-input__suffix .el-input__password')

        # ========== 提示信息 ==========
        self.error_message = page.locator(".el-message--error")
        self.success_message = page.locator(".el-message--success")

    # ========== 页面导航 ==========
    def goto(self):
        """导航到登录页面"""
        self.page.goto(self.URL)
        expect(self.username_input).to_be_visible(timeout=10000)
        return self

    # ========== 登录操作 ==========
    def login(self, username: str, password: str):
        """执行登录操作"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_btn.click()
        return self

    def toggle_password_visibility(self):
        """切换密码显示/隐藏"""
        self.eye_icon.click()
        return self

    def get_error_message(self) -> str:
        """获取错误提示信息"""
        expect(self.error_message).to_be_visible(timeout=5000)
        return self.error_message.inner_text()

    def is_error_displayed(self) -> bool:
        """判断是否显示错误提示"""
        return self.error_message.is_visible()
