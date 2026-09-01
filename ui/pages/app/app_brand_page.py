"""
App Brand Page Object
页面：品牌列表页（从首页"品牌制造商直供"进入）
职责：品牌列表页面元素定位和基础交互
"""

from playwright.sync_api import Page, expect
from config.settings import WEB_BASE_URL
from ui.pages.app.app_tabbar import AppTabBar
import re


class AppBrandPage:
    """App 品牌列表页面对象

    入口：首页 "品牌制造商直供" 区域点击右侧箭头进入
    """

    def __init__(self, page: Page):
        self.page = page
        self.tabbar = AppTabBar(page)

        # ========== 首页品牌制造商直供区域 ==========
        self.brand_section_header = page.locator("text=品牌制造商直供").first

        # ========== 品牌列表页元素 ==========
        self.brand_list = page.locator(".brand-list, .brand-item, .uni-list")

    # ========== 从首页导航到品牌列表 ==========
    def goto_brand_list_from_home(self):
        """从首页"品牌制造商直供"区域点击右侧箭头，进入推荐品牌列表页

        步骤：
        1. 确保在首页
        2. 滚动到"品牌制造商直供"区域
        3. 点击右侧箭头进入品牌列表页
        """
        # 确保在首页 tabbar 可见
        if not self.tabbar._is_visible():
            self.tabbar.back_to_tabbar()
        self.tabbar.click_home()

        # 滚动到品牌制造商直供区域
        expect(self.brand_section_header).to_be_visible(timeout=10000)
        self.brand_section_header.scroll_into_view_if_needed()

        # 点击右侧箭头（more 箭头），进入品牌列表页
        # 箭头通常在标题行的右侧，使用 >> 或 > 图标
        arrow = self.brand_section_header.locator(
            "xpath=ancestor::*[contains(@class,'f-header') or contains(@class,'header') or contains(@class,'section')][1]"
        ).locator("uni-text:last-child, .icon-right, .arrow, [class*='more'], [class*='right']").last
        # 如果箭头找不到，回退到点击标题行本身
        if arrow.count() > 0 and arrow.is_visible():
            arrow.click()
        else:
            self.brand_section_header.click()

        # 等待品牌列表页加载
        expect(self.page).to_have_url(re.compile(r"brand|home/brand"), timeout=10000)
        return self

    # ========== 品牌列表验证 ==========
    def brand_visible(self, brand_name: str) -> bool:
        """检查品牌列表中是否显示指定品牌"""
        brand = self.page.get_by_text(brand_name, exact=True).first
        return brand.is_visible()

    def verify_brand_visible(self, brand_name: str):
        """验证品牌列表中显示指定品牌"""
        brand = self.page.get_by_text(brand_name, exact=True).first
        expect(brand).to_be_visible(timeout=10000)
        return self

    def verify_brand_not_visible(self, brand_name: str):
        """验证品牌列表中不显示指定品牌"""
        brand = self.page.get_by_text(brand_name, exact=True).first
        expect(brand).not_to_be_visible(timeout=5000)
        return self
