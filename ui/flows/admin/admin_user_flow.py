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

    # ========== 新增用户流程 ==========
    def add_user(self, username: str, password: str, nickname: str, email: str):
        """新增用户

        Args:
            username: 帐号
            password: 密码
            nickname: 姓名
            email: 邮箱
        """
        self.admin_page.goto()
        self.admin_page.click_add()
        self.admin_page.fill_add_form(username, password, nickname, email)
        self.admin_page.save_add()
        return self

    # ========== 分配角色流程 ==========
    def assign_role(self, username: str, role_name: str):
        """为用户分配角色

        Args:
            username: 用户名
            role_name: 角色名称
        """
        self.admin_page.search(username)
        self.admin_page.click_assign_role_by_username(username)
        self.admin_page.select_role_in_dialog(role_name)
        self.admin_page.save_assign_role()
        return self

    # ========== 删除用户流程 ==========
    def delete_user(self, username: str):
        """删除指定用户

        Args:
            username: 要删除的用户名
        """
        self.admin_page.goto()
        self.admin_page.search(username)
        self.admin_page.click_delete_by_username(username)
        self.admin_page.confirm_delete()
        return self
