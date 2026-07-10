"""
登录功能测试用例
测试目标：http://localhost:8090/#/login
"""

import pytest
from playwright.sync_api import Page, expect
from ui.pages.admin.admin_login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """创建 LoginPage 实例"""
    lp = LoginPage(page)
    lp.goto()
    return lp


class TestLogin:
    """登录功能测试"""

    def test_login_wrong_password(self, login_page: LoginPage):
        """用户名正确，密码错误，提示密码不正确"""
        login_page.login("funx", "wrong_password")

        # 验证错误提示
        expect(login_page.error_message).to_contain_text("密码不正确")

    def test_login_wrong_username(self, login_page: LoginPage):
        """用户名错误，密码正确，提示用户名或密码错误"""
        login_page.login("wrong_user", "123456")

        # 验证错误提示
        expect(login_page.error_message).to_contain_text("用户名或密码错误")

    def test_password_visibility_toggle(self, login_page: LoginPage):
        """点击眼睛图标，显示密码，再次点击，隐藏密码"""
        login_page.password_input.fill("123456")

        # 初始状态：密码隐藏
        expect(login_page.password_input).to_have_attribute("type", "password")

        # 点击眼睛：密码显示
        login_page.toggle_password_visibility()
        expect(login_page.password_input).to_have_attribute("type", "text")

        # 再次点击眼睛：密码隐藏
        login_page.toggle_password_visibility()
        expect(login_page.password_input).to_have_attribute("type", "password")
