"""
用户列表测试用例
测试目标：http://localhost:8090/#/ums/admin
"""

from playwright.sync_api import Page, expect
from ui.flows.admin.admin_user_flow import AdminUserFlow
from utils.data_loader import load_yaml

# 加载测试数据（文件名与测试文件对应）
test_data = load_yaml("ui/test_user.yaml")


class TestUserSearch:
    """用户查询功能测试"""

    def test_search_by_username(self, logged_in_page: Page):
        """按帐号搜索用户"""
        data = test_data["test_search_by_username"]
        username = data["username"]

        flow = AdminUserFlow(logged_in_page)
        flow.search_user(username)

        # 验证搜索结果不为空
        expect(flow.admin_page.has_data()).to_be_visible()
        # 验证结果中包含搜索关键词
        expect(flow.admin_page.cell_contain_text(username)).to_be_visible()

    def test_disable_user(self, logged_in_page: Page):
        """编辑用户 - 将是否启用改为否，验证开关变灰色"""
        data = test_data["test_disable_user"]
        username = data["username"]

        flow = AdminUserFlow(logged_in_page)
        flow.search_user(username)

        # 点击编辑，将是否启用改为否
        flow.admin_page.click_edit_by_username(username)
        flow.admin_page.set_enabled(False)
        flow.admin_page.save_edit()

        # 验证开关变为灰色（未选中状态）
        switch = flow.admin_page.get_switch_by_username(username)
        expect(switch).not_to_have_class("el-switch is-checked")
        # 验证开关背景色为灰色
        core = switch.locator(".el-switch__core")
        expect(core).to_have_css("background-color", "rgb(220, 223, 230)")

        # 还原：将是否启用改回是
        flow.admin_page.click_edit_by_username(username)
        flow.admin_page.set_enabled(True)
        flow.admin_page.save_edit()
