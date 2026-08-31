"""
App Category Flow - Web App 商品分类业务流程
职责：组合页面操作，验证分类展示
"""

from playwright.sync_api import Page, expect
from ui.pages.app.app_category_page import AppCategoryPage


class AppCategoryFlow:
    """Web App 商品分类业务流程"""

    def __init__(self, page: Page):
        self.page = page
        self.category_page = AppCategoryPage(page)

    def goto_category(self):
        """导航到分类页面"""
        self.category_page.goto()
        return self

    def verify_parent_category(self, name: str):
        """验证左侧一级分类列表中存在指定分类

        Args:
            name: 一级分类名称
        """
        category = self.category_page.get_left_category(name)
        expect(category).to_be_visible(timeout=10000)
        return self

    def verify_child_category(self, parent_name: str, child_name: str):
        """点击左侧一级分类，验证右侧显示指定二级分类

        Args:
            parent_name: 一级分类名称
            child_name: 二级分类名称
        """
        self.category_page.click_left_category(parent_name)
        child = self.category_page.get_right_category(child_name)
        expect(child).to_be_visible(timeout=10000)
        return self
