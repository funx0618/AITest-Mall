"""
Admin Role List Page Object
页面：http://localhost:8090/#/ums/role
职责：只负责页面元素定位和基础交互，不包含业务逻辑
"""

from playwright.sync_api import Page, expect


class RolePage:
    """角色列表页面对象"""

    def __init__(self, page: Page):
        self.page = page

        # ========== 菜单导航 ==========
        self.hamburger = page.locator('svg.hamburger')
        self.menu_permission = page.get_by_role('menuitem', name='权限')
        self.menu_role_list = page.get_by_role('link', name='角色列表')

        # ========== 搜索区域 ==========
        self.search_input = page.get_by_placeholder("角色名称")
        self.search_btn = page.get_by_role("button", name="查询搜索")
        self.reset_btn = page.get_by_role("button", name="重置")

        # ========== 数据列表区域 ==========
        self.add_btn = page.get_by_role("button", name="添加")
        self.role_table = page.locator("table").nth(1)  # 第二个table是数据表
        self.table_cells = self.role_table.locator("tbody tr td")  # 所有数据单元格

        # ========== 添加弹窗 ==========
        self.add_dialog = page.locator('.el-dialog:has-text("添加角色")')
        self.add_name_input = self.add_dialog.locator('input').first
        self.add_desc_input = self.add_dialog.locator('textarea').first
        self.add_radio_enabled = self.add_dialog.locator('.el-radio:has-text("是")')
        self.add_radio_disabled = self.add_dialog.locator('.el-radio:has-text("否")')
        self.add_save_btn = self.add_dialog.get_by_role('button', name='确 定')

        # ========== 编辑弹窗 ==========
        self.edit_dialog = page.locator('.el-dialog:has-text("编辑角色")')
        self.radio_enabled = self.edit_dialog.locator('.el-radio:has-text("是")')
        self.radio_disabled = self.edit_dialog.locator('.el-radio:has-text("否")')
        self.save_btn = self.edit_dialog.get_by_role('button', name='确 定')

        # ========== 分配菜单弹窗 ==========
        self.assign_menu_dialog = page.locator('.el-dialog:has-text("分配菜单")')

        # ========== 分配资源弹窗 ==========
        self.assign_resource_dialog = page.locator('.el-dialog:has-text("分配资源")')

        # ========== 通用确认弹窗 ==========
        self.confirm_btn = page.locator('.el-message-box__btns button:has-text("确定")')

        # ========== 表格列头 ==========
        self.col_id = page.get_by_role("columnheader", name="编号")
        self.col_name = page.get_by_role("columnheader", name="名称")
        self.col_description = page.get_by_role("columnheader", name="描述")
        self.col_admin_count = page.get_by_role("columnheader", name="用户数")
        self.col_create_time = page.get_by_role("columnheader", name="添加时间")
        self.col_status = page.get_by_role("columnheader", name="是否启用")

    # ========== 页面导航 ==========
    def goto(self):
        """通过左侧菜单导航到角色列表页面"""
        # 如果菜单折叠，先展开
        if not self.menu_permission.is_visible():
            self.hamburger.click()
            expect(self.menu_permission).to_be_visible(timeout=5000)
        # 点击 权限 -> 角色列表
        self.menu_permission.click()
        self.menu_role_list.click()
        # 等待搜索框出现，确保页面加载完成
        expect(self.search_input).to_be_visible(timeout=15000)
        return self

    # ========== 搜索操作 ==========
    def search(self, keyword: str):
        """输入搜索关键词并点击查询"""
        self.search_input.fill(keyword)
        self.search_btn.click()
        # 等待表格数据刷新
        expect(self.search_btn).to_be_enabled(timeout=5000)
        return self

    def reset(self):
        """点击重置按钮"""
        self.reset_btn.click()
        expect(self.search_btn).to_be_enabled(timeout=5000)
        return self

    # ========== 表格数据获取 ==========
    def has_data(self):
        """判断表格是否有数据"""
        return self.table_cells.first

    def cell_contain_text(self, text: str):
        """获取包含指定文本的单元格"""
        return self.role_table.locator(f"tbody tr td:has-text('{text}')").first

    def get_all_rows(self):
        """获取表格所有数据行（过滤空行）"""
        all_rows = self.role_table.locator("tbody tr").all()
        return [row for row in all_rows if row.locator("td").count() > 0]

    def get_row_data(self, row) -> dict:
        """获取指定行的数据

        Args:
            row: Playwright Locator 行元素

        Returns:
            dict: 包含 id, name, description, admin_count, create_time 的字典
        """
        cells = row.locator("td").all()

        return {
            "id": cells[0].inner_text(),
            "name": cells[1].inner_text(),
            "description": cells[2].inner_text(),
            "admin_count": cells[3].inner_text(),
            "create_time": cells[4].inner_text(),
        }

    def get_all_row_data(self) -> list[dict]:
        """获取所有行的数据"""
        rows = self.get_all_rows()
        result = []
        for row in rows:
            result.append(self.get_row_data(row))
        return result

    # ========== 是否启用开关 ==========
    def get_switch_by_role_name(self, role_name: str):
        """根据角色名称获取该行的启用状态开关"""
        rows = self.role_table.locator('tbody tr').all()
        for row in rows:
            cells = row.locator('td').all()
            if len(cells) > 1 and cells[1].inner_text().strip() == role_name:
                return row.locator('.el-switch')
        return None

    # ========== 操作列按钮 ==========
    def click_edit_by_role_name(self, role_name: str):
        """根据角色名称找到对应行，点击编辑按钮"""
        rows = self.role_table.locator('tbody tr').all()
        for row in rows:
            cells = row.locator('td').all()
            if len(cells) > 1 and cells[1].inner_text().strip() == role_name:
                row.locator('button:has-text("编辑")').click()
                break
        expect(self.edit_dialog).to_be_visible(timeout=5000)
        return self

    def click_assign_menu_by_role_name(self, role_name: str):
        """根据角色名称找到对应行，点击分配菜单按钮"""
        rows = self.role_table.locator('tbody tr').all()
        for row in rows:
            cells = row.locator('td').all()
            if len(cells) > 1 and cells[1].inner_text().strip() == role_name:
                row.locator('button:has-text("分配菜单")').click()
                break
        expect(self.assign_menu_dialog).to_be_visible(timeout=5000)
        return self

    def click_assign_resource_by_role_name(self, role_name: str):
        """根据角色名称找到对应行，点击分配资源按钮"""
        rows = self.role_table.locator('tbody tr').all()
        for row in rows:
            cells = row.locator('td').all()
            if len(cells) > 1 and cells[1].inner_text().strip() == role_name:
                row.locator('button:has-text("分配资源")').click()
                break
        expect(self.assign_resource_dialog).to_be_visible(timeout=5000)
        return self

    def click_delete_by_role_name(self, role_name: str):
        """根据角色名称找到对应行，点击删除按钮"""
        rows = self.role_table.locator('tbody tr').all()
        for row in rows:
            cells = row.locator('td').all()
            if len(cells) > 1 and cells[1].inner_text().strip() == role_name:
                row.locator('button:has-text("删除")').click()
                break
        expect(self.confirm_btn).to_be_visible(timeout=5000)
        return self

    # ========== 添加弹窗操作 ==========
    def click_add(self):
        """点击添加按钮，打开添加弹窗"""
        self.add_btn.click()
        expect(self.add_dialog).to_be_visible(timeout=5000)
        return self

    def fill_add_form(self, name: str, description: str = "", enabled: bool = True):
        """填写添加角色表单

        Args:
            name: 角色名称
            description: 角色描述
            enabled: 是否启用，默认启用
        """
        self.add_name_input.fill(name)
        if description:
            self.add_desc_input.fill(description)
        if enabled:
            self.add_radio_enabled.click()
        else:
            self.add_radio_disabled.click()
        return self

    def save_add(self):
        """点击确定保存新增角色，并确认二次弹窗"""
        self.add_save_btn.click()
        self.confirm_btn.click()
        expect(self.add_dialog).to_be_hidden(timeout=5000)
        return self

    # ========== 编辑弹窗操作 ==========
    def set_enabled(self, enabled: bool):
        """在编辑弹窗中设置是否启用"""
        if enabled:
            self.radio_enabled.click()
        else:
            self.radio_disabled.click()
        return self

    def save_edit(self):
        """点击确定保存编辑"""
        self.save_btn.click()
        expect(self.edit_dialog).to_be_hidden(timeout=5000)
        return self

    def confirm_delete(self):
        """确认删除操作"""
        self.confirm_btn.click()
        expect(self.confirm_btn).to_be_hidden(timeout=5000)
        return self
