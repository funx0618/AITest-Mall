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

        # 验证优惠券状态为未过期
        flow.coupon_page.verify_coupon_status(coupon_name, data["status"])

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

    def test_add_expired_coupon_all_products(self, admin_logged_in_page: Page, app_logged_in: Page):
        """新增过期优惠券-全场通用，验证移动端商品详情页不可见"""
        data = test_data["test_add_expired_coupon_all_products"]
        coupon_name = data["coupon_name"]

        flow = CouponFlow(admin_logged_in_page)
        flow.add_coupon(
            name=data["coupon_name"],
            platform=data["platform"],
            total=data["total"],
            amount=data["amount"],
            threshold=data["threshold"],
            validity_days_before=data["validity_days_before"],
            validity_days_after=data["validity_days_after"],
        )

        # 搜索验证新增优惠券已创建
        flow.coupon_page.goto_list()
        flow.coupon_page.search(coupon_name)
        expect(flow.coupon_page.cell_contain_text(coupon_name)).to_be_visible()

        # 验证优惠券状态为已过期
        flow.coupon_page.verify_coupon_status(coupon_name, data["status"])

        # --- App 端验证：过期的全场通用优惠券不应显示 ---
        app_product = AppProductPage(app_logged_in)
        app_product.goto_product(data["product_id"])
        app_product.verify_coupon_not_visible(coupon_name)

        # 删除优惠券，还原数据
        flow.coupon_page.click_delete_by_name(coupon_name)
        # 重新搜索验证优惠券已删除 - 查询结果应显示"暂无数据"
        flow.coupon_page.search(coupon_name)
        expect(flow.coupon_page.page.locator('text=暂无数据')).to_be_visible(timeout=10000)

    def test_threshold_not_met_coupon(self, admin_logged_in_page: Page, app_logged_in: Page):
        """新增高门槛优惠券-指定商品，未达门槛的商品不可见"""
        data = test_data["test_threshold_not_met_coupon"]
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

        # --- App 端验证：未达使用门槛的商品不可见 ---
        app_product = AppProductPage(app_logged_in)
        app_product.goto_product(data["specified_product_id"])
        app_product.verify_coupon_not_visible(coupon_name)

        # 删除优惠券，还原数据
        flow.coupon_page.click_delete_by_name(coupon_name)
        # 重新搜索验证优惠券已删除 - 查询结果应显示"暂无数据"
        flow.coupon_page.search(coupon_name)
        expect(flow.coupon_page.page.locator('text=暂无数据')).to_be_visible(timeout=10000)

    def test_edit_coupon_category(self, admin_logged_in_page: Page, app_logged_in: Page):
        """新增指定分类优惠券-编辑修改名称，验证同一用户再次领取提示已领取。
        领取限制是基于优惠券维度（couponId + memberId）"""
        data = test_data["test_edit_coupon_category"]
        coupon_name = data["coupon_name"]
        new_coupon_name = data["new_coupon_name"]

        flow = CouponFlow(admin_logged_in_page)

        # --- 步骤1：新增指定分类为"家用电器-电视"的优惠券 ---
        flow.add_coupon(
            name=data["coupon_name"],
            platform=data["platform"],
            total=data["total"],
            amount=data["amount"],
            threshold=data["threshold"],
            category_parent=data["category_parent"],
            category_child=data["category_child"],
        )

        # 搜索验证新增优惠券已创建
        flow.coupon_page.goto_list()
        flow.coupon_page.search(coupon_name)
        expect(flow.coupon_page.cell_contain_text(coupon_name)).to_be_visible()

        # --- 步骤2：App端验证商品33（电视）可领取 ---
        app_product = AppProductPage(app_logged_in)
        app_product.goto_product(data["claim_product_id"])
        app_product.claim_coupon(coupon_name)

        # --- 步骤3：编辑优惠券，仅修改名称（保留原分类不变） ---
        flow.edit_coupon(
            coupon_name=coupon_name,
            new_name=new_coupon_name,
        )

        # 搜索验证优惠券名称已修改
        flow.coupon_page.goto_list()
        flow.coupon_page.search(new_coupon_name)
        expect(flow.coupon_page.cell_contain_text(new_coupon_name)).to_be_visible()

        # --- 步骤4：App端验证商品33再次领取提示已领取 ---
        app_product.goto_product(data["claim_product_id"])
        app_product.verify_already_claimed(new_coupon_name)

        # 删除优惠券，还原数据
        flow.coupon_page.click_delete_by_name(new_coupon_name)
        # 重新搜索验证优惠券已删除 - 查询结果应显示"暂无数据"
        flow.coupon_page.search(new_coupon_name)
        expect(flow.coupon_page.page.locator('text=暂无数据')).to_be_visible(timeout=10000)
