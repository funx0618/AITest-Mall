"""
App Home / Search Page Object
页面：http://localhost:8060/#/
职责：首页搜索和导航
"""

from playwright.sync_api import Page, expect
from config.settings import WEB_BASE_URL


class AppHomePage:
    """App 首页 / 搜索页对象"""

    URL = WEB_BASE_URL + "/#"
    SEARCH_URL = WEB_BASE_URL + "/#/pages/product/search"

    def __init__(self, page: Page):
        self.page = page

        # ========== 搜索页元素（搜索页才有可用的 input） ==========
        self.search_input = page.get_by_role("searchbox")
        self.search_submit_btn = page.locator(".search-btn, [class*='search'] [class*='btn'], [class*='search-btn']")
        self.no_more = page.locator("text=没有更多了")

        # ========== 底部导航 ==========
        self.nav_home = page.get_by_text("首页", exact=True)
        self.nav_cart = page.get_by_text("购物车", exact=True)
        self.nav_my = page.get_by_text("我的", exact=True)

    # ========== 页面导航 ==========
    def goto(self):
        """导航到首页"""
        self.page.goto(self.URL)
        return self

    # ========== 搜索操作 ==========
    def search(self, keyword: str):
        """导航到搜索页，输入关键词并搜索"""
        self.page.goto(self.SEARCH_URL)
        expect(self.search_input).to_be_visible(timeout=10000)
        self.search_input.fill(keyword)
        # 使用回车键触发搜索，避免点击到错误的"搜索"文本
        self.search_input.press("Enter")
        # 等待商品列表加载
        expect(self.no_more).to_be_visible(timeout=15000)
        return self

    def click_product_by_name(self, name: str):
        """在搜索结果中点击包含指定名称的商品"""
        self.page.locator(f"text={name}").first.click()
        return self
