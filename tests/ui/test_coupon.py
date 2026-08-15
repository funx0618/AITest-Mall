"""
优惠券列表测试用例
测试目标：http://localhost:8090/#/sms/coupon
"""

from playwright.sync_api import Page, expect
from ui.flows.admin.coupon_flow import CouponFlow
from ui.pages.app.app_product_page import AppProductPage
from utils.data_loader import load_yaml

# 加载测试数据（文件名与测试文件对应）
test_data = load_yaml("ui/test_coupon.yaml")


class TestCoupon:
    """优惠券新增功能测试"""

    def test_add_coupon_specified_claim(self, admin_logged_in_page: Page, app_logged_in: Page):
        """新增优惠券-指定商品领取验证"""
        data = test_data["test_add_coupon_specified_claim"]
        coupon_name = data["coupon_name"]

        flow = CouponFlow(admin_logged_in_page)
        flow.add_coupon(
            name=data["coupon_name"],
            platform=data["platform"],
            total=data["total"],
            amount=data["amount"],
            threshold=data["threshold"],
            product_name=data["product_name"],
        )

        # 搜索验证新增优惠券已创建
        flow.coupon_page.goto_list()
        flow.coupon_page.search(coupon_name)
        expect(flow.coupon_page.cell_contain_text(coupon_name)).to_be_visible()

        # --- App 端验证：指定商品可领取 ---
        app_product = AppProductPage(app_logged_in)
        app_product.goto_product(data["specified_product_id"])
        app_product.claim_coupon(coupon_name)

        # --- App 端验证：非指定商品不可见 ---
        app_product.goto_product(data["other_product_id"])
        app_product.verify_coupon_not_visible(coupon_name)

        # 删除优惠券，还原数据
        flow.coupon_page.click_delete_by_name(coupon_name)
        # 重新搜索验证优惠券已删除 - 查询结果应显示"暂无数据"
        flow.coupon_page.search(coupon_name)
        expect(flow.coupon_page.page.locator('text=暂无数据')).to_be_visible(timeout=10000)
