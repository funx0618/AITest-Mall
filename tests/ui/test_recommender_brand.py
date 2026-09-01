"""
品牌推荐测试用例
测试目标：http://localhost:8090/#/sms/homeBrand
"""

from playwright.sync_api import Page, expect
from ui.flows.admin.brand_recommend_flow import BrandRecommendFlow
from ui.pages.admin.brand_recommend_page import BrandRecommendPage
from ui.pages.app.app_brand_page import AppBrandPage
from utils.data_loader import load_yaml

# 加载测试数据（文件名与测试文件对应）
test_data = load_yaml("ui/test_recommender_brand.yaml")


class TestRecommenderBrand:
    """品牌推荐功能测试"""

    def test_disable_brand_recommend_not_in_app(self, admin_logged_in_page: Page, app_logged_in: Page):
        """关闭小米的推荐，验证 App 推荐品牌页面不展示小米

        步骤：
        1. 进入 admin 菜单营销下的品牌推荐，将小米的是否推荐按钮关闭
        2. 验证小米的状态更新为未推荐
        3. 登录 app，定位到品牌制造商直供部分，点击右边的箭头，进入推荐品牌页面
        4. 验证品牌中没有小米
        """
        data = test_data["test_disable_brand_recommend_not_in_app"]
        brand_name = data["brand_name"]

        admin_flow = BrandRecommendFlow(admin_logged_in_page)
        admin_page = BrandRecommendPage(admin_logged_in_page)
        app_brand = AppBrandPage(app_logged_in)

        # ========== 步骤1~2：关闭推荐并验证状态 ==========
        # 使用 idempotent 方法确保关闭推荐（无论当前状态如何）
        admin_flow.disable_brand_recommend(brand_name)

        # 验证推荐开关已关闭
        expect(admin_page.get_row_by_name(brand_name).locator('.el-switch')).not_to_have_class(
            "el-switch is-checked"
        )

        # 验证状态文本为"未推荐"
        expect(admin_page.get_recommend_status_cell(brand_name)).to_contain_text("未推荐")

        # ========== 步骤3~4：App 端验证 + 还原（try/finally 确保还原） ==========
        try:
            app_brand.goto_brand_list_from_home()
            app_brand.verify_brand_not_visible(brand_name)
        finally:
            # 还原：重新开启推荐
            admin_flow.enable_brand_recommend(brand_name)

    def test_enable_brand_recommend_shown_in_app(self, admin_logged_in_page: Page, app_logged_in: Page):
        """开启小米的推荐，验证 App 推荐品牌页面展示小米

        步骤：
        1. 进入 admin 菜单营销下的品牌推荐，将小米的是否推荐按钮打开
        2. 验证小米的状态更新为推荐中
        3. 登录 app，定位到品牌制造商直供部分，点击右边的箭头，进入推荐品牌页面
        4. 验证品牌中有小米
        """
        data = test_data["test_enable_brand_recommend_shown_in_app"]
        brand_name = data["brand_name"]

        admin_flow = BrandRecommendFlow(admin_logged_in_page)
        admin_page = BrandRecommendPage(admin_logged_in_page)
        app_brand = AppBrandPage(app_logged_in)

        # ========== 步骤1~2：开启推荐并验证状态 ==========
        # 使用 idempotent 方法确保开启推荐（无论当前状态如何）
        admin_flow.enable_brand_recommend(brand_name)

        # 验证推荐开关已开启
        expect(admin_page.get_row_by_name(brand_name).locator('.el-switch')).to_have_class(
            "el-switch is-checked"
        )

        # 验证状态文本为"推荐中"
        expect(admin_page.get_recommend_status_cell(brand_name)).to_contain_text("推荐中")

        # ========== 步骤3~4：App 端验证 + 还原（try/finally 确保还原） ==========
        try:
            app_brand.goto_brand_list_from_home()
            app_brand.verify_brand_visible(brand_name)
        finally:
            # 还原：重新关闭推荐
            admin_flow.disable_brand_recommend(brand_name)
