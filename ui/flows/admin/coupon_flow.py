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
        category_parent: str = None,
        category_child: str = None,
        validity_days_before: int = 0,
        validity_days_after: int = 30,
    ):
        """新增优惠券

        Args:
            name: 优惠券名称
            platform: 适用平台，默认"全平台"
            total: 总发行量，默认"1"
            amount: 面额，默认"10"
            threshold: 使用门槛（满X元可用），默认"100"
            product_name: 指定商品名称，None 表示全场通用
            category_parent: 一级分类名称（如"家用电器"），与 category_child 配合使用
            category_child: 二级分类名称（如"电视"），与 category_parent 配合使用
            validity_days_before: 有效期开始日期偏移（今天往前N天），默认0
            validity_days_after: 有效期结束日期偏移（今天往后N天），默认30
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

        # 设置有效期
        self.coupon_page.set_validity_days(validity_days_before, validity_days_after)

        # 选择可使用商品
        if product_name:
            self.coupon_page.select_specified_product()
            self.coupon_page.search_and_add_product(product_name)
        elif category_parent and category_child:
            self.coupon_page.select_specified_category()
            self.coupon_page.select_category(category_parent, category_child)

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

    # ========== 编辑优惠券流程 ==========
    def edit_coupon(
        self,
        coupon_name: str,
        new_name: str = None,
        category_parent: str = None,
        category_child: str = None,
    ):
        """编辑优惠券

        Args:
            coupon_name: 要编辑的优惠券名称
            new_name: 新的优惠券名称，None 表示不修改
            category_parent: 新的一级分类名称，None 表示不修改
            category_child: 新的二级分类名称，None 表示不修改
        """
        self.coupon_page.goto_list()
        self.coupon_page.search(coupon_name)
        self.coupon_page.click_edit_by_name(coupon_name)

        # 修改优惠券名称
        if new_name:
            self.coupon_page.fill_name(new_name)

        # 修改指定分类
        if category_parent and category_child:
            # 先删除已有的分类
            self.coupon_page.remove_all_categories()
            # 选择指定分类并添加新分类
            self.coupon_page.select_specified_category()
            self.coupon_page.select_category(category_parent, category_child)

        # 提交
        self.coupon_page.submit()
        return self
