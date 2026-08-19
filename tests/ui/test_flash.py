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

    def test_time(self):
        from datetime import datetime, timezone, timedelta
        SHANGHAI_TZ = timezone(timedelta(hours=8))
        current_hour = datetime.now(SHANGHAI_TZ).hour
        print(f"Current hour: {current_hour}")
        if 8 <= current_hour < 10:
                    return "8:00"
        elif 10 <= current_hour < 12:
            return "10:00"
        elif 12 <= current_hour < 14:
            return "12:00"
        elif 14 <= current_hour < 16:
            return "14:00"
        elif 16 <= current_hour < 18:
            return "16:00"
        elif 18 <= current_hour < 20:
            return "18:00"
        elif 20 <= current_hour < 22:
            return "20:00"
        else:
            return "8:00"