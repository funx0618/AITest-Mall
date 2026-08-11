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
        self.menu_role_list = page.get_by_role('menu').get_by_role('link', name='角色列表')

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

        # ========== 分配菜单页面（独立页面，非弹窗） ==========
        self.assign_menu_tree = page.locator('.el-tree')
        self.assign_menu_save_btn = page.get_by_role('button', name='保存')

        # ========== 分配资源页面（独立页面，非弹窗） ==========
        self.assign_resource_container = page.locator('.app-container')
        self.assign_resource_save_btn = page.get_by_role('button', name='保存')

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
        """通过左侧菜单导航到角色列表页面（幂等：已在目标页面则跳过导航）"""
        if self.search_input.is_visible():
            return self
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
        # 等待表格加载完成：有数据时等 td 渲染，无数据时等空态提示
        first_td = self.role_table.locator('tbody tr').first.locator('td').nth(4)
        empty_hint = self.page.locator('.el-table__empty-text, .el-table__empty-block')
        expect(first_td.or_(empty_hint)).to_be_attached(timeout=10000)
        return self

    def wait_for_role_in_table(self, role_name: str, timeout: int = 10000):
        """等待指定角色出现在表格中"""
        expect(
            self.role_table.locator(f'tbody tr td:nth-child(2):has-text("{role_name}")').first
        ).to_be_visible(timeout=timeout)

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
        """获取表格所有数据行（过滤空行和不完整的行）"""
        all_rows = self.role_table.locator("tbody tr").all()
        return [row for row in all_rows if row.locator("td").count() >= 5]

    def get_row_data(self, row) -> dict:
        """获取指定行的数据

        Args:
            row: Playwright Locator 行元素

        Returns:
            dict: 包含 id, name, description, admin_count, create_time 的字典
        """
        # 等待行内 td 渲染完成，至少5列才是有效数据行
        td_count = row.locator("td").count()
        if td_count < 5:
            return None
        cells = row.locator("td").all()
        if len(cells) < 5:
            return None

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
            data = self.get_row_data(row)
            if data:
                result.append(data)
        return result

    # ========== 是否启用开关 ==========
    def get_switch_by_role_name(self, role_name: str):
        """根据角色名称获取该行的启用状态开关"""
        row = self.role_table.locator(f'tbody tr:has(td:nth-child(2):has-text("{role_name}"))').first
        if row.count():
            return row.locator('.el-switch')
        return None

    # ========== 操作列按钮 ==========
    def click_edit_by_role_name(self, role_name: str):
        """根据角色名称找到对应行，点击编辑按钮"""
        row = self.role_table.locator(f'tbody tr:has(td:nth-child(2):has-text("{role_name}"))').first
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("编辑")').click()
        expect(self.edit_dialog).to_be_visible(timeout=5000)
        return self

    def click_assign_menu_by_role_name(self, role_name: str):
        """根据角色名称找到对应行，点击分配菜单按钮（导航到分配菜单页面）"""
        row = self.role_table.locator(f'tbody tr:has(td:nth-child(2):has-text("{role_name}"))').first
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("分配菜单")').click()
        # 分配菜单是独立页面，等待页面上的树加载完成
        expect(self.assign_menu_tree).to_be_visible(timeout=10000)
        return self

    def click_assign_resource_by_role_name(self, role_name: str):
        """根据角色名称找到对应行，点击分配资源按钮（导航到分配资源页面）"""
        row = self.role_table.locator(f'tbody tr:has(td:nth-child(2):has-text("{role_name}"))').first
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("分配资源")').click()
        # 分配资源是独立页面，等待保存按钮出现确认页面加载完成
        expect(self.assign_resource_save_btn).to_be_visible(timeout=10000)
        return self

    def click_delete_by_role_name(self, role_name: str):
        """根据角色名称找到对应行，点击删除按钮"""
        row = self.role_table.locator(f'tbody tr:has(td:nth-child(2):has-text("{role_name}"))').first
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("删除")').click()
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

    # ========== 分配菜单弹窗操作 ==========
    def select_menu_item(self, menu_name: str):
        """在分配菜单弹窗中，勾选指定菜单项（按文本匹配）"""
        node = self.assign_menu_tree.locator(f'.el-tree-node:has(.el-tree-node__label:has-text("{menu_name}"))')
        checkbox = node.locator('.el-checkbox').first
        if not checkbox.locator('.is-checked').count():
            checkbox.click()
        return self

    def unselect_menu_item(self, menu_name: str):
        """在分配菜单弹窗中，取消勾选指定菜单项"""
        node = self.assign_menu_tree.locator(f'.el-tree-node:has(.el-tree-node__label:has-text("{menu_name}"))')
        checkbox = node.locator('.el-checkbox').first
        if checkbox.locator('.is-checked').count():
            checkbox.click()
        return self

    def unselect_all_menus(self):
        """取消所有已勾选的菜单项"""
        checked = self.assign_menu_tree.locator('.el-checkbox.is-checked').first
        while checked.count():
            checked.click()
            checked = self.assign_menu_tree.locator('.el-checkbox.is-checked').first
        return self

    def expand_menu_node(self, menu_name: str):
        """展开指定菜单节点"""
        node = self.assign_menu_tree.locator(f'.el-tree-node:has(.el-tree-node__label:has-text("{menu_name}"))')
        arrow = node.locator('.el-tree-node__expand-icon').first
        if arrow.count() and 'is-leaf' not in (arrow.get_attribute('class') or ''):
            arrow.click()
        return self

    def save_assign_menu(self):
        """保存分配菜单，确认二次弹窗，等待返回角色列表页面"""
        self.assign_menu_save_btn.click()
        self.confirm_btn.click()
        # 保存后导航回角色列表页面，等待搜索框出现
        expect(self.search_input).to_be_visible(timeout=10000)
        return self

    # ========== 分配资源页面操作 ==========
    def select_resource_item(self, resource_name: str):
        """在分配资源页面中，勾选指定资源模块（按文本模糊匹配，如"营销"匹配"营销模块"）"""
        label = self.page.locator(f'.el-checkbox__label:has-text("{resource_name}")').first
        label.click()
        return self

    def unselect_all_resources(self):
        """点击清空按钮取消所有已勾选的资源项"""
        clear_btn = self.page.get_by_role('button', name='清空')
        if clear_btn.is_visible():
            clear_btn.click()
            self.confirm_btn.click()
            expect(self.confirm_btn).to_be_hidden(timeout=5000)
        return self

    def expand_resource_node(self, resource_name: str):
        """展开指定资源节点（资源页面无树结构，无需展开）"""
        return self

    def save_assign_resource(self):
        """保存分配资源，确认二次弹窗，等待返回角色列表页面"""
        self.assign_resource_save_btn.click()
        self.confirm_btn.click()
        # 保存后导航回角色列表页面，等待搜索框出现
        expect(self.search_input).to_be_visible(timeout=10000)
        return self
