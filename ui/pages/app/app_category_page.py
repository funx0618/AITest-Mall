"""
App Category Page Object
页面：http://localhost:8060/#/pages/category/category
职责：商品分类页面元素定位和基础交互（左侧父分类 + 右侧子分类）
"""

from playwright.sync_api import Page, expect
from config.settings import WEB_BASE_URL
from ui.pages.app.app_tabbar import AppTabBar


class AppCategoryPage:
    """App 商品分类页面对象

    页面结构：左侧一级分类列表 + 右侧二级分类列表
    """

    URL = WEB_BASE_URL + "/#/pages/category/category"

    def __init__(self, page: Page):
        self.page = page
        self.tabbar = AppTabBar(page)

        # ========== 左侧一级分类列表 ==========
        # uni-app 分类页：.left-aside > .f-item
        self.left_items = page.locator(".left-aside .f-item")

        # ========== 右侧二级分类列表 ==========
        # uni-app 分类页：.right-aside .s-item > uni-text
        self.right_items = page.locator(".right-aside .s-item")

    # ========== 页面导航 ==========
    def goto(self):
        """通过底部导航或直接 URL 进入分类页面"""
        if not self.tabbar._is_visible():
            self.tabbar.back_to_tabbar()
        # 尝试点击分类 tab（如果有），否则通过 URL 导航
        category_tab = self.tabbar.tabbar.locator(".uni-tabbar__item").filter(has_text="分类")
        if category_tab.count() > 0:
            category_tab.click()
        else:
            self.page.goto(self.URL)
        return self

    # ========== 左侧一级分类操作 ==========
    def get_left_category(self, name: str):
        """获取左侧指定名称的一级分类元素"""
        return self.left_items.filter(has_text=name).first

    def click_left_category(self, name: str):
        """点击左侧指定名称的一级分类

        Args:
            name: 一级分类名称
        """
        category = self.get_left_category(name)
        expect(category).to_be_visible(timeout=10000)
        category.click()
        return self

    # ========== 右侧二级分类操作 ==========
    def get_right_category(self, name: str):
        """获取右侧指定名称的二级分类元素"""
        return self.right_items.filter(has_text=name).first

    def right_category_visible(self, name: str) -> bool:
        """检查右侧是否显示指定名称的二级分类"""
        return self.get_right_category(name).is_visible()
