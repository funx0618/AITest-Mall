"""
App Home / Search Page Object
页面：http://localhost:8060/#/
职责：首页搜索和导航
"""

from playwright.sync_api import Page, expect
from config.settings import WEB_BASE_URL
import re


class AppHomePage:
    """App 首页 / 搜索页对象"""

    URL = WEB_BASE_URL + "/#"

    def __init__(self, page: Page):
        self.page = page

        # ========== 首页搜索框（点击进入搜索页） ==========
        self.search_entry = page.locator(".uni-page-head-search")

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
        """点击首页搜索框进入搜索页，输入关键词并搜索"""
        self.goto()
        self.search_entry.click()
        expect(self.page).to_have_url(re.compile("search"), timeout=10000)
        expect(self.search_input).to_be_visible(timeout=10000)
        self.search_input.fill(keyword)
        # 使用回车键触发搜索，避免点击到错误的"搜索"文本
        self.search_input.press("Enter")
        # 等待商品列表加载
        expect(self.no_more).to_be_visible(timeout=15000)
        return self

    def click_product_by_name(self, name: str):
        """在搜索结果中点击包含指定名称的商品（排除搜索历史等干扰）"""
        # 等待页面跳转到商品列表页
        expect(self.page).to_have_url(re.compile(r"product/list"), timeout=10000)
        # 使用 .goods-item 定位商品卡片，避免误点搜索历史
        product_card = self.page.locator(".goods-item").filter(
            has=self.page.get_by_text(name, exact=True)
        )
        expect(product_card).to_be_visible(timeout=10000)
        product_card.click()
        return self

    # ========== 秒杀专区验证 ==========
    def scroll_to_flash_sale(self):
        """滚动到秒杀专区"""
        flash_sale_section = self.page.locator("text=秒杀专区").first
        flash_sale_section.scroll_into_view_if_needed()
        expect(flash_sale_section).to_be_visible(timeout=10000)
        return self

    def verify_flash_sale_product_visible(self, product_name: str):
        """验证秒杀专区中显示指定商品"""
        # 先刷新页面确保数据同步
        self.page.reload()
        self.scroll_to_flash_sale()
        # 秒杀专区的商品名称文本应可见
        expect(self.page.get_by_text(product_name, exact=True)).to_be_visible(timeout=10000)
        return self
