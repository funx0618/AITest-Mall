"""
Role Flow - 角色列表业务流程
职责：组合页面操作，实现业务场景
"""

from playwright.sync_api import Page
from ui.pages.admin.role_page import RolePage


class RoleFlow:
    """角色列表业务流程"""

    def __init__(self, page: Page):
        self.page = page
        self.role_page = RolePage(page)

    # ========== 查询流程 ==========
    def search_role(self, keyword: str) -> list[dict]:
        """搜索角色并返回结果

        Args:
            keyword: 搜索关键词（角色名称）

        Returns:
            list[dict]: 匹配的角色列表
        """
        self.role_page.goto()
        self.role_page.search(keyword)
        return self.role_page.get_all_row_data()

    # ========== 新增角色流程 ==========
    def add_role(self, name: str, description: str = "", enabled: bool = True):
        """新增角色

        Args:
            name: 角色名称
            description: 角色描述
            enabled: 是否启用，默认启用
        """
        self.role_page.goto()
        self.role_page.click_add()
        self.role_page.fill_add_form(name, description, enabled)
        self.role_page.save_add()
        return self

    # ========== 删除角色流程 ==========
    def delete_role(self, role_name: str):
        """删除指定角色

        Args:
            role_name: 要删除的角色名称
        """
        self.role_page.search(role_name)
        self.role_page.click_delete_by_role_name(role_name)
        self.role_page.confirm_delete()
        return self
