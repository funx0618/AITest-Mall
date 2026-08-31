"""
Admin Product Category Page Object
页面：http://localhost:8090/#/pms/productCate
职责：只负责页面元素定位和基础交互，不包含业务逻辑
"""

from playwright.sync_api import Page, expect


class ProductCategoryPage:
    """商品分类页面对象"""

    def __init__(self, page: Page):
        self.page = page

        # ========== 菜单导航 ==========
        self.hamburger = page.locator('svg.hamburger')
        self.menu_product = page.get_by_role('menuitem', name='商品', exact=True)
        self.menu_category = page.get_by_role('menu').get_by_role('link', name='商品分类')

        # ========== 数据列表页面（#/pms/productCate）==========
        self.add_btn = page.get_by_role("button", name="添加")
        self.data_table = page.locator("table").nth(1)

        # ========== 添加分类页面（#/pms/addProductCate）==========
        # 注意：添加分类是独立页面，非弹窗
        self.form_name_input = page.get_by_role('textbox', name='* 分类名称：')
        self.form_parent_select = page.get_by_role('combobox', name='上级分类：')
        self.form_sort_input = page.locator('.el-form-item:has-text("排序") input')
        self.form_show_yes = page.locator('.el-form-item:has(.el-form-item__label:has-text("是否显示")):not(:has(.el-form-item__label:has-text("导航栏"))) label.el-radio:has-text("是")')
        self.form_show_no = page.locator('.el-form-item:has(.el-form-item__label:has-text("是否显示")):not(:has(.el-form-item__label:has-text("导航栏"))) label.el-radio:has-text("否")')
        self.form_nav_yes = page.locator('.el-form-item:has(.el-form-item__label:has-text("导航栏")) label.el-radio:has-text("是")')
        self.form_submit_btn = page.get_by_role('button', name='提交')
        self.form_reset_btn = page.get_by_role('button', name='重置')

        # ========== 编辑分类页面（#/pms/updateProductCate/:id）==========
        self.edit_name_input = page.get_by_role('textbox', name='* 分类名称：')
        self.edit_submit_btn = page.get_by_role('button', name='提交')

        # ========== 确认弹窗 ==========
        self.confirm_btn = page.locator('.el-message-box__btns button:has-text("确定")')

        # ========== 表格列头 ==========
        self.col_id = page.get_by_role("columnheader", name="编号")
        self.col_name = page.get_by_role("columnheader", name="分类名称")
        self.col_level = page.get_by_role("columnheader", name="级别")
        self.col_sort = page.get_by_role("columnheader", name="排序")
        self.col_show = page.get_by_role("columnheader", name="是否显示")
        self.col_nav = page.get_by_role("columnheader", name="导航栏")

    # ========== 列表页面导航 ==========
    def goto(self):
        """通过左侧菜单导航到商品分类根列表页面（始终强制导航，确保回到根列表）"""
        if not self.menu_product.is_visible():
            self.hamburger.click()
            expect(self.menu_product).to_be_visible()
        self.menu_product.click()
        self.menu_category.click()
        expect(self.add_btn).to_be_visible(timeout=15000)
        return self

    # ========== 表格数据 ==========
    def cell_contain_text(self, text: str):
        """获取包含指定文本的单元格"""
        return self.data_table.locator(f"tbody tr td:has-text('{text}')").first

    def get_row_by_name(self, name: str):
        """根据分类名称获取行"""
        return self.data_table.locator(
            f'tbody tr:has(td:has-text("{name}"))'
        ).first

    # ========== 添加分类（跳转到独立页面） ==========
    def goto_add_page(self):
        """点击添加按钮，跳转到添加分类页面"""
        self.add_btn.click()
        expect(self.form_name_input).to_be_visible(timeout=15000)
        return self

    def fill_form_name(self, name: str):
        """填写分类名称"""
        self.form_name_input.clear()
        self.form_name_input.fill(name)
        return self

    def select_form_parent(self, parent_name: str):
        """在添加页面选择上级分类

        Args:
            parent_name: 上级分类名称
        """
        # 点击 el-select wrapper 打开下拉（combobox input 被 placeholder 遮挡）
        self.page.locator('.el-form-item:has-text("上级分类") .el-select__wrapper').click()
        option = self.page.locator(
            f'.el-select-dropdown:visible .el-select-dropdown__item:has-text("{parent_name}")'
        ).first
        expect(option).to_be_visible(timeout=5000)
        option.click()
        return self

    def select_form_show(self, show: bool = True):
        """设置是否显示

        Args:
            show: True=是, False=否
        """
        # 使用 Playwright 建议的定位方式：先定位 radiogroup，再定位 label
        group = self.page.get_by_role('radiogroup', name='是否显示：')
        if show:
            group.locator('label').filter(has_text='是').click()
        else:
            group.locator('label').filter(has_text='否').click()
        return self

    def submit_form(self):
        """点击提交按钮，处理确认弹窗，等待返回列表页"""
        # 提交按钮在页面底部，先滚动到可见区域
        self.form_submit_btn.scroll_into_view_if_needed()
        self.form_submit_btn.click()
        # 处理确认弹窗
        expect(self.confirm_btn).to_be_visible(timeout=5000)
        self.confirm_btn.click()
        expect(self.confirm_btn).to_be_hidden(timeout=5000)
        # 等待成功提示出现
        success_msg = self.page.locator('.el-message--success')
        expect(success_msg).to_be_visible(timeout=10000)
        # 通过侧边栏菜单导航回商品分类列表
        self.page.get_by_role('menuitem', name='商品分类').click()
        expect(self.add_btn).to_be_visible(timeout=15000)
        return self

    # ========== 查看下级操作 ==========
    def click_view_children(self, category_name: str):
        """根据分类名称找到对应行，点击查看下级按钮

        Args:
            category_name: 分类名称
        """
        row = self.get_row_by_name(category_name)
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("查看下级")').click()
        expect(self.add_btn).to_be_visible(timeout=15000)
        return self

    # ========== 编辑操作 ==========
    def click_edit_by_name(self, category_name: str):
        """根据分类名称找到对应行，点击编辑按钮（跳转到编辑页面）"""
        row = self.get_row_by_name(category_name)
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("编辑")').click()
        expect(self.edit_name_input).to_be_visible(timeout=15000)
        return self

    def submit_edit(self):
        """点击提交按钮保存编辑，等待返回列表页"""
        self.edit_submit_btn.click()
        expect(self.add_btn).to_be_visible(timeout=15000)
        return self

    # ========== 删除操作 ==========
    def click_delete_by_name(self, category_name: str):
        """根据分类名称找到对应行，点击删除按钮"""
        row = self.get_row_by_name(category_name)
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("删除")').click()
        expect(self.confirm_btn).to_be_visible(timeout=5000)
        self.confirm_btn.click()
        expect(self.confirm_btn).to_be_hidden(timeout=5000)
        return self
