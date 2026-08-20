"""
Seckill Flow - 秒杀业务流程
职责：组合页面操作，实现业务场景
"""

from datetime import date, timedelta
from playwright.sync_api import Page
from ui.pages.admin.flash_page import FlashPage, FlashSessionPage, FlashProductPage


class FlashFlow:
    """秒杀业务流程"""

    def __init__(self, page: Page):
        self.page = page
        self.flash_page = FlashPage(page)
        self.session_page = FlashSessionPage(page)
        self.product_page = FlashProductPage(page)

    # ========== 新增秒杀活动流程 ==========
    def add_flash_sale(self, title: str):
        """新增秒杀活动，开始时间选择当天，结束时间选择后一天，上线/下线选择上线

        Args:
            title: 活动标题
        """
        today_str = date.today().strftime("%Y-%m-%d")
        tomorrow_str = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.flash_page.goto_list()
        self.flash_page.open_add_dialog()
        self.flash_page.fill_activity_title(title)
        self.flash_page.set_start_time(today_str)
        self.flash_page.set_end_time(tomorrow_str)
        self.flash_page.select_online()
        self.flash_page.confirm_add()
        return self

    # ========== 删除秒杀时间段流程 ==========
    def delete_flash_session(self, session_name: str):
        """删除指定秒杀时间段

        Args:
            session_name: 时间段名称，如 "23:00"
        """
        self.flash_page.goto_list()
        self.flash_page.click_session_list()
        self.session_page.click_delete_session_by_name(session_name)
        return self

    # ========== 设置秒杀商品流程 ==========
    def set_flash_product(self, activity_name: str, product_name: str, session_name: str = None):
        """为秒杀活动设置商品

        Args:
            activity_name: 活动名称
            product_name: 商品名称
            session_name: 时间段名称，None 时自动获取当前时间所属的时间段
        """
        if session_name is None:
            session_name = self.session_page.get_current_session_name()
        self.flash_page.goto_list()
        self.flash_page.search(activity_name)
        self.flash_page.click_set_product_by_name(activity_name)
        self.session_page.click_product_list(session_name)
        self.product_page.open_add_product_dialog()
        self.product_page.search_and_select_product(product_name)
        self.product_page.confirm_select()
        return self

    # ========== 删除秒杀活动流程 ==========
    def delete_flash_sale(self, activity_name: str):
        """删除指定秒杀活动

        Args:
            activity_name: 活动名称
        """
        self.flash_page.goto_list()
        self.flash_page.search(activity_name)
        self.flash_page.click_delete_by_name(activity_name)
        return self

    # ========== 新增秒杀时间段流程 ==========
    def add_flash_session(self, session_name: str,
                          start_time: str, end_time: str):
        """在秒杀时间段页面添加时间段

        Args:
            session_name: 时间段名称，如 "23:00"
            start_time: 每日开始时间，如 "23:00:00"
            end_time: 每日结束时间，如 "24:00:00"
        """
        self.flash_page.goto_list()
        self.flash_page.click_session_list()
        self.session_page.open_add_dialog()
        self.session_page.fill_session_name(session_name)
        self.session_page.set_session_start_time(start_time)
        self.session_page.set_session_end_time(end_time)
        self.session_page.confirm_add_session()
        return self
