"""
Pytest 全局 conftest
"""

import re
import pytest
from playwright.sync_api import Page, expect
from config.settings import LOGIN_URL, DEFAULT_USERNAME, DEFAULT_PASSWORD
from ui.pages.login_page import LoginPage


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
    # 等待登录成功，跳转到首页
    expect(page).to_have_url(re.compile(r".*#/home"), timeout=15000)
    return page
