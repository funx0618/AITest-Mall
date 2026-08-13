"""
Coupon Flow - 优惠券业务流程
职责：组合页面操作，实现业务场景
"""

from datetime import date, timedelta
from playwright.sync_api import Page
from ui.pages.admin.coupon_page import CouponPage


class CouponFlow:
    """优惠券业务流程"""

    def __init__(self, page: Page):
        self.page = page
        self.coupon_page = CouponPage(page)

    # ========== 查询流程 ==========
    def search_coupon(self, keyword: str):
        """搜索优惠券

        Args:
            keyword: 搜索关键词（优惠券名称）
        """
        self.coupon_page.goto_list()
        self.coupon_page.search(keyword)
        return self.coupon_page.has_data()

    # ========== 新增优惠券流程 ==========
    def add_coupon(
        self,
        name: str,
        platform: str = "全平台",
        total: str = "1",
        amount: str = "10",
        threshold: str = "100",
        product_name: str = None,
    ):
        """新增优惠券

        Args:
            name: 优惠券名称
            platform: 适用平台，默认"全平台"
            total: 总发行量，默认"1"
            amount: 面额，默认"10"
            threshold: 使用门槛（满X元可用），默认"100"
            product_name: 指定商品名称，None 表示全场通用
        """
        self.coupon_page.goto_add()

        # 填写基本信息
        self.coupon_page.fill_name(name)
        self.coupon_page.select_platform(platform)
        self.coupon_page.fill_total(total)
        self.coupon_page.fill_amount(amount)
        self.coupon_page.fill_threshold(threshold)

        # 设置领取日期为今天
        self.coupon_page.set_claim_date_today()

        # 设置有效期：今天开始，往后30天
        self.coupon_page.set_validity_days(0, 30)

        # 选择可使用商品
        if product_name:
            self.coupon_page.select_specified_product()
            self.coupon_page.search_and_add_product(product_name)

        # 提交
        self.coupon_page.submit()
        return self

    # ========== 删除流程 ==========
    def delete_coupon(self, coupon_name: str):
        """删除指定优惠券

        Args:
            coupon_name: 优惠券名称
        """
        self.coupon_page.goto_list()
        self.coupon_page.search(coupon_name)
        self.coupon_page.click_delete_by_name(coupon_name)
        return self
