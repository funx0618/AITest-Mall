"""
App Home / Search Page Object
页面：http://localhost:8060/#/
职责：首页搜索和导航
"""

from playwright.sync_api import Page, expect
from config.settings import WEB_BASE_URL
from ui.pages.app.app_tabbar import AppTabBar
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
        self.tabbar = AppTabBar(page)

    # ========== 页面导航 ==========
    def goto(self):
        """通过底部导航进入首页，tabbar 不可见时通过返回箭头回到 tabbar 页面"""
        if not self.tabbar._is_visible():
            self.tabbar.back_to_tabbar()
        self.tabbar.click_home()
        expect(self.search_entry).to_be_visible(timeout=10000)
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

    def _flash_sale_section(self):
        """获取秒杀专区的商品列表区域

        DOM 结构：.f-header.m-t（标题） 和 .guess-section（商品列表）是 .container 下的兄弟节点
        通过标题定位，取其下一个兄弟节点作为商品区域
        """
        flash_header = self.page.locator(".f-header.m-t").filter(has_text="秒杀专区")
        return flash_header.locator("xpath=following-sibling::uni-view[1]")

    def verify_flash_sale_product_visible(self, product_name: str):
        """验证秒杀专区中显示指定商品"""
        self.page.reload()
        self.scroll_to_flash_sale()
        section = self._flash_sale_section()
        expect(section.get_by_text(product_name, exact=True).first).to_be_visible(timeout=10000)
        return self

    def click_flash_sale_product(self, product_name: str):
        """点击秒杀专区中的指定商品，进入商品详情页

        Args:
            product_name: 商品名称
        """
        self.page.reload()
        self.scroll_to_flash_sale()
        section = self._flash_sale_section()
        product_item = section.get_by_text(product_name, exact=True).first
        expect(product_item).to_be_visible(timeout=10000)
        product_item.click()
        return self
