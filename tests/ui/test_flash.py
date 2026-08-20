"""
秒杀活动测试用例
测试目标：http://localhost:8090/#/sms/flash
"""

from time import timezone

from playwright.sync_api import Page, expect
from ui.flows.admin.flash_flow import FlashFlow
from ui.pages.app.app_home_page import AppHomePage
from utils.data_loader import load_yaml

# 加载测试数据（文件名与测试文件对应）
test_data = load_yaml("ui/test_flash.yaml")


class TestFlash:
    """秒杀活动功能测试"""

    def test_add_flash_sale_and_verify_app(self, admin_logged_in_page: Page, app_logged_in: Page):
        """新增秒杀活动-设置商品-App端秒杀专区验证"""
        data = test_data["test_add_flash_sale_and_verify_app"]
        activity_title = data["activity_title"]
        product_name = data["product_name"]

        flow = FlashFlow(admin_logged_in_page)

        # 步骤1：新增秒杀活动（开始时间和结束时间都选择当天，上线/下线选择上线）
        flow.add_flash_sale(title=activity_title)

        # 搜索验证新增秒杀活动已创建
        flow.flash_page.goto_list()
        flow.flash_page.search(activity_title)
        expect(flow.flash_page.cell_contain_text(activity_title)).to_be_visible()

        # 步骤2：设置商品，选择当前所属的时间段，设置商品为小米电视4A
        flow.set_flash_product(
            activity_name=activity_title,
            product_name=product_name,
        )

        # 步骤3：App端验证秒杀专区中显示对应商品
        app_home = AppHomePage(app_logged_in)
        app_home.goto()
        app_home.verify_flash_sale_product_visible(product_name)



        # 删除秒杀活动，还原数据
        flow.delete_flash_sale(activity_title)
        flow.flash_page.search(activity_title)
        expect(flow.flash_page.page.locator('text=暂无数据')).to_be_visible(timeout=10000)

    def test_disabled_session_not_visible_in_product_list(self, admin_logged_in_page: Page):
        """验证禁用的秒杀时间段在设置商品时不显示"""
        data = test_data["test_disabled_session_not_visible_in_product_list"]
        activity_title = data["activity_title"]
        session_name = data["session_name"]
        start_time = data["start_time"]
        end_time = data["end_time"]

        flow = FlashFlow(admin_logged_in_page)

        # # 步骤1：新增秒杀活动
        flow.add_flash_sale(title=activity_title)

        # 搜索验证新增秒杀活动已创建
        flow.flash_page.goto_list()
        flow.flash_page.search(activity_title)
        expect(flow.flash_page.cell_contain_text(activity_title)).to_be_visible()

        # 步骤2：进入秒杀时间段页面，添加禁用的新时间段
        flow.add_flash_session(
            session_name=session_name,
            start_time=start_time,
            end_time=end_time,
        )
        # 验证新时间段已在列表中显示
        flow.session_page.verify_session_visible(session_name)

        # 步骤3：回到秒杀活动列表，点击设置商品，验证禁用时间段不显示
        flow.flash_page.goto_list()
        flow.flash_page.search(activity_title)
        flow.flash_page.click_set_product_by_name(activity_title)
        flow.session_page.verify_session_not_visible(session_name)

        # 清理：删除秒杀活动和新增的时间段（先刷新页面，确保菜单导航可用）
        admin_logged_in_page.reload()
        flow.flash_page.goto_list()
        flow.delete_flash_sale(activity_title)
        flow.flash_page.search(activity_title)
        expect(flow.flash_page.page.locator('text=暂无数据')).to_be_visible(timeout=10000)
        flow.delete_flash_session(session_name)

