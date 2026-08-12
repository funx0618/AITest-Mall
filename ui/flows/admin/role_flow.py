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
        self.role_page.goto()
        self.role_page.search(role_name)
        self.role_page.click_delete_by_role_name(role_name)
        self.role_page.confirm_delete()
        return self

    # ========== 分配菜单流程 ==========
    def assign_menu(self, role_name: str, menu_names: list[str], expand_only: list[str] | None = None):
        """为角色分配菜单

        Args:
            role_name: 角色名称
            menu_names: 要勾选的菜单名称列表
            expand_only: 仅展开不勾选的父节点名称列表（用于展开子菜单前需要先展开父节点的场景）
        """
        self.role_page.search(role_name)
        self.role_page.click_assign_menu_by_role_name(role_name)
        # 先取消所有已勾选的菜单
        self.role_page.unselect_all_menus()
        # 展开需要展开但不勾选的父节点
        for parent_name in (expand_only or []):
            self.role_page.expand_menu_node(parent_name)
            # 展开可能意外触发父节点复选框，取消父节点及其子节点的勾选
            self.role_page.unselect_menu_item(parent_name)
        # 展开并勾选指定菜单
        for menu_name in menu_names:
            self.role_page.expand_menu_node(menu_name)
            self.role_page.select_menu_item(menu_name)
        # 验证：确保只有指定的菜单被勾选
        checked = self.role_page.get_checked_menu_names()
        assert sorted(checked) == sorted(menu_names), \
            f"菜单分配异常：期望勾选 {menu_names}，实际勾选了 {checked}"
        self.role_page.save_assign_menu()
        return self

    # ========== 取消分配菜单流程 ==========
    def unassign_all_menus(self, role_name: str):
        """取消角色的所有菜单分配

        Args:
            role_name: 角色名称
        """
        self.role_page.search(role_name)
        self.role_page.click_assign_menu_by_role_name(role_name)
        self.role_page.unselect_all_menus()
        self.role_page.save_assign_menu()
        return self

    # ========== 分配资源流程 ==========
    def assign_resource(self, role_name: str, resource_names: list[str]):
        """为角色分配资源（新角色资源默认为空，直接勾选即可）

        Args:
            role_name: 角色名称
            resource_names: 要分配的资源名称列表
        """
        self.role_page.search(role_name)
        self.role_page.click_assign_resource_by_role_name(role_name)
        # 勾选指定资源模块
        for resource_name in resource_names:
            self.role_page.select_resource_item(resource_name)
        self.role_page.save_assign_resource()
        return self
