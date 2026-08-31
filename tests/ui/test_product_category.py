"""
商品分类测试用例
测试目标：http://localhost:8090/#/pms/productCate
"""

from playwright.sync_api import Page, expect
from ui.flows.admin.product_category_flow import ProductCategoryFlow
from ui.flows.app.app_category_flow import AppCategoryFlow
from utils.data_loader import load_yaml

# 加载测试数据（文件名与测试文件对应）
test_data = load_yaml("ui/test_product_category.yaml")


class TestProductCategory:
    """商品分类功能测试"""

    def test_add_root_and_child_category_verify_in_app(self, admin_logged_in_page: Page, app_logged_in: Page):
        """新增父分类和子分类后，在 Web App 分类页验证展示

        步骤：
        1. 新增商品分类，无上级分类，是否显示选择是，新增成功
        2. 新增成功后，点击此分类的查看下级按钮，增加子分类，上级分类选择新增的分类
        3. 进入 Web App 分类页，验证左侧显示父分类，点击后显示子分类
        """
        data = test_data["test_add_root_and_child_category_verify_in_app"]
        parent_name = data["parent_name"]
        child_name = data["child_name"]
        show = data["show"]

        admin_flow = ProductCategoryFlow(admin_logged_in_page)
        app_flow = AppCategoryFlow(app_logged_in)

        # ========== 步骤1：新增顶级分类 ==========
        admin_flow.add_root_category(name=parent_name, show=show)

        # 验证新增成功：分类名称出现在列表中
        expect(admin_flow.category_page.cell_contain_text(parent_name)).to_be_visible()

        # ========== 步骤2：查看下级并新增子分类 ==========
        admin_flow.add_child_category(parent_name=parent_name, child_name=child_name, show=show)
        # submit_form 已导航回根列表，需重新点击查看下级进入子分类列表
        admin_flow.category_page.click_view_children(parent_name)

        # 验证子分类新增成功：在下级列表中出现子分类名称
        expect(admin_flow.category_page.cell_contain_text(child_name)).to_be_visible()

        # ========== 步骤3：在 Web App 分类页验证（与清理放在 try-finally 中） ==========
        try:
            app_flow.goto_category()
            # 验证左侧一级分类列表中显示父分类
            app_flow.verify_parent_category(parent_name)
            # 点击父分类，验证右侧显示子分类
            app_flow.verify_child_category(parent_name, child_name)
        finally:
            admin_flow.category_page.click_delete_by_name(child_name)
            admin_flow.category_page.goto()
            admin_flow.category_page.click_delete_by_name(parent_name)

    def test_add_hidden_root_category_not_shown_in_app(self, admin_logged_in_page: Page, app_logged_in: Page):
        """新增父分类（是否显示=否），验证在 Web App 分类页不展示

        步骤：
        1. 新增商品分类，无上级分类，是否显示选择否，新增成功
        2. 进入 Web App 分类页，验证左侧一级分类列表中不显示该分类
        """
        data = test_data["test_add_hidden_root_category_not_shown_in_app"]
        parent_name = data["parent_name"]
        show = data["show"]

        admin_flow = ProductCategoryFlow(admin_logged_in_page)
        app_flow = AppCategoryFlow(app_logged_in)

        # ========== 步骤1：新增顶级分类（是否显示=否） ==========
        admin_flow.add_root_category(name=parent_name, show=show)

        # 验证新增成功：分类名称出现在后台列表中
        expect(admin_flow.category_page.cell_contain_text(parent_name)).to_be_visible()

        # ========== 步骤2：在 Web App 分类页验证不展示（与清理放在 try-finally 中） ==========
        try:
            app_flow.goto_category()
            # 验证左侧一级分类列表中不显示该分类
            left_item = app_flow.category_page.get_left_category(parent_name)
            expect(left_item).not_to_be_visible()
        finally:
            # admin 页面仍在根列表，无需 goto
            admin_flow.category_page.click_delete_by_name(parent_name)

