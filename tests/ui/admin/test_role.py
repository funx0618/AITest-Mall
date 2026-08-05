"""
角色列表测试用例
测试目标：http://localhost:8090/#/ums/role
"""

from playwright.sync_api import Page, expect
from ui.flows.admin.role_flow import RoleFlow
from utils.data_loader import load_yaml

# 加载测试数据（文件名与测试文件对应）
test_data = load_yaml("ui/test_role.yaml")


class TestRoleAdd:
    """角色新增功能测试"""

    def test_add_role(self, admin_logged_in_page: Page):
        """新增角色 - 添加营销管理员，验证后删除"""
        data = test_data["test_add_role"]
        role_name = data["role_name"]
        description = data["description"]

        flow = RoleFlow(admin_logged_in_page)
        flow.add_role(role_name, description)

        # 搜索验证新增角色已创建
        flow.role_page.search(role_name)
        expect(flow.role_page.cell_contain_text(role_name)).to_be_visible()

        # 删除角色，还原数据
        flow.role_page.click_delete_by_role_name(role_name)
        flow.role_page.confirm_delete()
        # 验证角色已删除
        flow.role_page.search(role_name)
        expect(flow.role_page.cell_contain_text(role_name)).to_be_hidden(timeout=5000)
