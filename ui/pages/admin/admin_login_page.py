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
        self.eye_icon = page.locator(".el-input:has(input[name='password']) .el-input__password")

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
        """获取错误提示文本（适用于错误提示持续显示的场景）

        会先等待 .el-message--error 出现，再返回 inner_text()。
        如果提示一闪而过，应改用 error_message_containing()。
        """
        expect(self.error_message).to_be_visible(timeout=5000)
        return self.error_message.inner_text()

    def is_error_displayed(self) -> bool:
        """判断错误提示是否可见（瞬时快照，无等待）

        直接返回当前时刻 .el-message--error 的可见状态，不做轮询等待。
        适合在已有其他等待之后快速检查，或用于 if 分支判断。
        """
        return self.error_message.is_visible()

    def error_message_containing(self, text: str):
        """返回匹配指定文本的错误提示定位器（适用于一闪而过的提示）

        返回 Locator（不等待），需配合 expect(...).to_be_visible(timeout) 使用。
        Playwright 会持续轮询，直到同时匹配 .el-message--error 样式和指定文本。
        比先 get_error_message() 再比对文本更快、更不容易错过短暂提示。

        用法：
            expect(login_page.error_message_containing("帐号已被禁用")).to_be_visible(timeout=5000)
        """
        return self.page.locator(f'.el-message--error:has-text("{text}")')
