"""
Brand Recommend Flow - 品牌推荐业务流程
职责：组合页面操作，实现业务场景
"""

from playwright.sync_api import Page
from ui.pages.admin.brand_recommend_page import BrandRecommendPage
from ui.pages.app.app_brand_page import AppBrandPage


class BrandRecommendFlow:
    """品牌推荐业务流程"""

    def __init__(self, page: Page):
        self.page = page
        self.brand_page = BrandRecommendPage(page)

    # ========== 切换品牌推荐状态 ==========
    def toggle_brand_recommend(self, brand_name: str):
        """在品牌推荐列表中切换指定品牌的推荐状态

        Args:
            brand_name: 品牌名称
        """
        self.brand_page.goto_list()
        self.brand_page.search(brand_name)
        self.brand_page.toggle_recommend_by_name(brand_name)
        return self

    # ========== 设置品牌推荐 ==========
    def enable_brand_recommend(self, brand_name: str):
        """开启品牌推荐（若当前已开启则跳过）

        Args:
            brand_name: 品牌名称
        """
        self.brand_page.goto_list()
        self.brand_page.search(brand_name)
        if not self.brand_page.is_recommend_on_by_name(brand_name):
            self.brand_page.toggle_recommend_by_name(brand_name)
        return self

    # ========== 取消品牌推荐 ==========
    def disable_brand_recommend(self, brand_name: str):
        """关闭品牌推荐（若当前已关闭则跳过）

        Args:
            brand_name: 品牌名称
        """
        self.brand_page.goto_list()
        self.brand_page.search(brand_name)
        if self.brand_page.is_recommend_on_by_name(brand_name):
            self.brand_page.toggle_recommend_by_name(brand_name)
        return self
