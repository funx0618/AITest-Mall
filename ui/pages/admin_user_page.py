"""
Admin User List Page Object
页面：http://localhost:8090/#/ums/admin
职责：只负责页面元素定位和基础交互，不包含业务逻辑
"""

from playwright.sync_api import Page, expect


class AdminUserPage:
    """用户列表页面对象"""

    def __init__(self, page: Page):
        self.page = page

        # ========== 菜单导航 ==========
        self.hamburger = page.locator('svg.hamburger')
        self.menu_permission = page.get_by_role('menuitem', name='权限')
        self.menu_user_list = page.get_by_role('link', name='用户列表')

        # ========== 搜索区域 ==========
        self.search_input = page.get_by_placeholder("帐号/姓名")
        self.search_btn = page.get_by_role("button", name="查询搜索")
        self.reset_btn = page.get_by_role("button", name="重置")

        # ========== 数据列表区域 ==========
        self.add_btn = page.get_by_role("button", name="添加")
        self.user_table = page.locator("table").nth(1)  # 第二个table是数据表
        self.table_cells = self.user_table.locator("tbody tr td")  # 所有数据单元格

        # ========== 编辑弹窗 ==========
        self.edit_dialog = page.locator('.el-dialog:has-text("编辑用户")')
        self.radio_enabled = self.edit_dialog.locator('.el-radio:has-text("是")')
        self.radio_disabled = self.edit_dialog.locator('.el-radio:has-text("否")')
        self.save_btn = self.edit_dialog.get_by_role('button', name='确 定')
        self.confirm_btn = page.locator('.el-message-box__btns button:has-text("确定")')

        # ========== 表格列头 ==========
        self.col_id = page.get_by_role("columnheader", name="编号")
        self.col_username = page.get_by_role("columnheader", name="帐号")
        self.col_nickname = page.get_by_role("columnheader", name="姓名")
        self.col_email = page.get_by_role("columnheader", name="邮箱")
        self.col_create_time = page.get_by_role("columnheader", name="添加时间")
        self.col_login_time = page.get_by_role("columnheader", name="最后登录")
        self.col_status = page.get_by_role("columnheader", name="是否启用")

    # ========== 页面导航 ==========
    def goto(self):
        """通过左侧菜单导航到用户列表页面"""
        # 如果菜单折叠，先展开
        if not self.menu_permission.is_visible():
            self.hamburger.click()
            expect(self.menu_permission).to_be_visible(timeout=5000)
        # 点击 权限 -> 用户列表
        self.menu_permission.click()
        self.menu_user_list.click()
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

    # ========== 表格数据获取 ==========
    def has_data(self):
        """判断表格是否有数据"""
        return self.table_cells.first

    def cell_contain_text(self, text: str):
        """获取包含指定文本的单元格"""
        return self.user_table.locator(f"tbody tr td:has-text('{text}')").first

    def get_switch_by_username(self, username: str):
        """根据用户名获取该行的启用状态开关"""
        rows = self.user_table.locator('tbody tr').all()
        for row in rows:
            cells = row.locator('td').all()
            if len(cells) > 1 and cells[1].inner_text().strip() == username:
                return row.locator('.el-switch')
        return None

    def click_edit_by_username(self, username: str):
        """根据用户名找到对应行，点击编辑按钮"""
        rows = self.user_table.locator('tbody tr').all()
        for row in rows:
            cells = row.locator('td').all()
            if len(cells) > 1 and cells[1].inner_text().strip() == username:
                row.locator('button:has-text("编辑")').click()
                break
        expect(self.edit_dialog).to_be_visible(timeout=5000)
        return self

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
        self.confirm_btn.click()
        expect(self.edit_dialog).to_be_hidden(timeout=5000)
        return self

    def get_all_rows(self):
        """获取表格所有数据行（过滤空行）"""
        all_rows = self.user_table.locator("tbody tr").all()
        # 过滤掉没有 td 的行（可能是空占位行）
        return [row for row in all_rows if row.locator("td").count() > 0]

    def get_row_data(self, row_index: int = 0) -> dict:
        """获取指定行的数据

        Args:
            row_index: 行索引，从0开始

        Returns:
            dict: 包含 id, username, nickname, email, create_time, login_time 的字典
        """
        row = self.user_table.locator("tbody tr").nth(row_index)
        cells = row.locator("td").all()

        return {
            "id": cells[0].inner_text(),
            "username": cells[1].inner_text(),
            "nickname": cells[2].inner_text(),
            "email": cells[3].inner_text(),
            "create_time": cells[4].inner_text(),
            "login_time": cells[5].inner_text(),
        }

    def get_all_row_data(self) -> list[dict]:
        """获取所有行的数据"""
        rows = self.get_all_rows()
        result = []
        for i in range(len(rows)):
            result.append(self.get_row_data(i))
        return result


