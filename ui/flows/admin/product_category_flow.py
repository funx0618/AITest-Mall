"""
Product Category Flow - 商品分类业务流程
职责：组合页面操作，实现业务场景
"""

from playwright.sync_api import Page
from ui.pages.admin.product_category_page import ProductCategoryPage


class ProductCategoryFlow:
    """商品分类业务流程"""

    def __init__(self, page: Page):
        self.page = page
        self.category_page = ProductCategoryPage(page)

    # ========== 新增分类流程（无上级分类） ==========
    def add_root_category(self, name: str, show: bool = True, sort: str = "0"):
        """新增顶级分类（无上级分类）

        Args:
            name: 分类名称
            show: 是否显示，默认 True
            sort: 排序，默认 "0"
        """
        self.category_page.goto()
        self.category_page.goto_add_page()
        self.category_page.fill_form_name(name)
        self.category_page.select_form_show(show)
        self.category_page.submit_form()
        return self

    # ========== 查看下级并新增子分类流程 ==========
    def add_child_category(self, parent_name: str, child_name: str, show: bool = True, sort: str = "0"):
        """查看指定分类的下级，并在下级页面新增子分类

        Args:
            parent_name: 父级分类名称
            child_name: 子分类名称
            show: 是否显示，默认 True
            sort: 排序，默认 "0"
        """
        # 点击查看下级按钮
        self.category_page.click_view_children(parent_name)
        # 在下级分类页面新增子分类，选择上级分类为父分类
        self.category_page.goto_add_page()
        self.category_page.fill_form_name(child_name)
        self.category_page.select_form_parent(parent_name)
        self.category_page.select_form_show(show)
        self.category_page.submit_form()
        return self

    # ========== 删除分类流程 ==========
    def delete_category(self, name: str):
        """删除指定分类

        Args:
            name: 分类名称
        """
        self.category_page.goto()
        self.category_page.click_delete_by_name(name)
        return self
