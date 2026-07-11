"""
Pytest 全局 conftest
"""

import re
import pytest
from playwright.sync_api import Page, Browser, BrowserContext, expect
from config.settings import LOGIN_URL, DEFAULT_USERNAME, DEFAULT_PASSWORD, WEB_USERNAME, WEB_PASSWORD
from ui.pages.admin.admin_login_page import LoginPage
from ui.pages.app.app_login_page import AppLoginPage

# Web App 手机端视窗配置 (iPhone 12)
MOBILE_VIEWPORT = {"width": 375, "height": 812}
MOBILE_USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/15.0 Mobile/15E148 Safari/604.1"
)


@pytest.fixture
def admin_logged_in_page(page: Page) -> Page:
    """后台管理登录后的 page fixture"""
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
    # 等待登录成功，跳转到首页
    expect(page).to_have_url(re.compile(r".*#/home"), timeout=15000)
    return page


@pytest.fixture
def app_context(browser: Browser):
    """为 Web App 创建独立的手机端浏览器上下文"""
    context = browser.new_context(
        viewport=MOBILE_VIEWPORT,
        user_agent=MOBILE_USER_AGENT,
        is_mobile=True,
        has_touch=True,
    )
    yield context
    context.close()


@pytest.fixture
def app_page(app_context):
    """为 Web App 创建独立的手机端页面"""
    page = app_context.new_page()
    yield page
    page.close()


@pytest.fixture
def app_logged_in(app_page: Page) -> Page:
    """Web App 登录后的 page fixture"""
    login_page = AppLoginPage(app_page)
    login_page.goto()
    login_page.login(WEB_USERNAME, WEB_PASSWORD)
    expect(app_page).to_have_url(re.compile(r".*#/$"), timeout=15000)
    return app_page
