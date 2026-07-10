"""
Admin User Flow - 用户列表业务流程
职责：组合页面操作，实现业务场景
"""

from playwright.sync_api import Page
from ui.pages.admin.admin_user_page import AdminUserPage


class AdminUserFlow:
    """用户列表业务流程"""

    def __init__(self, page: Page):
        self.page = page
        self.admin_page = AdminUserPage(page)

    # ========== 查询流程 ==========
    def search_user(self, keyword: str) -> list[dict]:
        """搜索用户并返回结果

        Args:
            keyword: 搜索关键词（帐号/姓名）

        Returns:
            list[dict]: 匹配的用户列表
        """
        self.admin_page.goto()
        self.admin_page.search(keyword)
        return self.admin_page.get_all_row_data()
