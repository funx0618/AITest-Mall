"""
Pytest 全局 conftest
"""

import re
import pytest
from playwright.sync_api import Page, Browser, Playwright, expect
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD, WEB_USERNAME, WEB_PASSWORD, ADMIN_API_BASE_URL, APP_API_BASE_URL
from ui.pages.admin.admin_login_page import LoginPage
from ui.pages.app.app_login_page import AppLoginPage
from api.admin.login_service import LoginService
from api.app.login import AppLoginService
from utils.db.db_client import DBClient

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


@pytest.fixture
def admin_token(playwright: Playwright) -> str:
    """通过 SSO 登录获取后台管理 token"""
    api_context = playwright.request.new_context(base_url=ADMIN_API_BASE_URL)
    try:
        service = LoginService(api_context)
        resp = service.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        assert resp.ok, f"登录请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"登录失败: {resp.json}"
        data = resp.data
        token_head = data.get("tokenHead", "")
        token = data.get("token", "")
        assert token, f"登录未返回token: {resp.json}"
        return f"{token_head}{token}"
    finally:
        api_context.dispose()


@pytest.fixture
def admin_api_context(playwright: Playwright, admin_token: str):
    """后台管理 API 请求上下文（已携带 token）"""
    api_context = playwright.request.new_context(
        base_url=ADMIN_API_BASE_URL,
        extra_http_headers={"Authorization": f"Bearer {admin_token}"},
    )
    yield api_context
    api_context.dispose()


@pytest.fixture
def app_token(playwright: Playwright) -> str:
    """通过 SSO 登录获取前台商城 token"""
    api_context = playwright.request.new_context(base_url=APP_API_BASE_URL)
    try:
        service = AppLoginService(api_context)
        resp = service.login(WEB_USERNAME, WEB_PASSWORD)
        assert resp.ok, f"登录请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"登录失败: {resp.json}"
        data = resp.data
        token_head = data.get("tokenHead", "")
        token = data.get("token", "")
        assert token, f"登录未返回token: {resp.json}"
        return f"{token_head}{token}"
    finally:
        api_context.dispose()


@pytest.fixture
def app_api_context(playwright: Playwright, app_token: str):
    """前台商城 API 请求上下文（已携带 token）"""
    api_context = playwright.request.new_context(
        base_url=APP_API_BASE_URL,
        extra_http_headers={"Authorization": f"Bearer {app_token}"},
    )
    yield api_context
    api_context.dispose()


@pytest.fixture(scope="session")
def db():
    """数据库客户端实例（整个测试会话共享一个连接，autocommit=True 保证无快照问题）"""
    client = DBClient()
    yield client
    client.close()


# ========== 测试数据初始化 ==========
PRODUCT_IDS = (26, 30, 33)


@pytest.fixture(scope="session", autouse=True)
def ensure_test_products(db):
    """确保测试商品数据存在：逐个检查 id=26,30,33，仅对缺失的商品执行 SQL 插入"""
    import os

    existing = db.query(
        "SELECT id FROM pms_product WHERE id IN %s", (PRODUCT_IDS,)
    )
    existing_ids = {row["id"] for row in existing}
    missing = set(PRODUCT_IDS) - existing_ids

    if not missing:
        print(f"[ensure_test_products] 商品 {PRODUCT_IDS} 均已存在，跳过插入")
        return

    sql_dir = os.path.join(os.path.dirname(__file__), "data", "sql")
    for pid in sorted(missing):
        sql_file = os.path.join(sql_dir, f"product_insert_{pid}.sql")
        print(f"[ensure_test_products] 缺失商品 id={pid}，执行 {os.path.basename(sql_file)} ...")
        with open(sql_file, "r", encoding="utf-8") as f:
            db.execute_script(f.read())

    print(f"[ensure_test_products] 完成，共插入 {len(missing)} 个商品")
