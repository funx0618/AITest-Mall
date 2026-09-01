"""
Admin Brand Recommend Page Object
页面：http://localhost:8090/#/sms/homeBrand
职责：只负责页面元素定位和基础交互，不包含业务逻辑
"""

from playwright.sync_api import Page, expect


class BrandRecommendPage:
    """品牌推荐列表页面对象"""

    def __init__(self, page: Page):
        self.page = page

        # ========== 菜单导航 ==========
        self.hamburger = page.locator('svg.hamburger')
        self.menu_marketing = page.get_by_role('menuitem', name='营销')
        self.menu_brand_recommend = page.get_by_role('menu').get_by_role('link', name='品牌推荐')

        # ========== 搜索区域 ==========
        self.search_input = page.get_by_placeholder("品牌名称")
        self.search_btn = page.get_by_role("button", name="查询搜索")
        self.reset_btn = page.get_by_role("button", name="重置")

        # ========== 数据列表区域 ==========
        self.data_table = page.locator("table").nth(1)  # 第二个table是数据表

    # ========== 页面导航 ==========
    def goto_list(self):
        """通过左侧菜单导航到品牌推荐列表页面（幂等）"""
        if self.search_input.is_visible():
            return self
        if not self.menu_marketing.is_visible():
            self.hamburger.click()
            expect(self.menu_marketing).to_be_visible()
        self.menu_marketing.click()
        self.menu_brand_recommend.click()
        expect(self.search_input).to_be_visible(timeout=15000)
        return self

    # ========== 搜索操作 ==========
    def search(self, keyword: str):
        """输入品牌名称并点击查询"""
        self.search_input.fill(keyword)
        self.search_btn.click()
        first_td = self.data_table.locator('tbody tr').first.locator('td').nth(1)
        empty_hint = self.page.locator('.el-table__empty-text').first
        expect(first_td.or_(empty_hint)).to_be_attached(timeout=10000)
        return self

    # ========== 表格数据 ==========
    def get_row_by_name(self, name: str):
        """根据品牌名称获取行"""
        return self.data_table.locator(
            f'tbody tr:has(td:has-text("{name}"))'
        ).first

    def cell_contain_text(self, text: str):
        """获取包含指定文本的单元格"""
        return self.data_table.locator(f"tbody tr td:has-text('{text}')").first

    # ========== 推荐开关操作 ==========
    def toggle_recommend_by_name(self, name: str):
        """根据品牌名称找到对应行，点击推荐状态开关

        开关是 el-switch 组件，直接点击 el-switch__core 即可切换状态。
        切换后会弹出确认提示框，需点击确定。
        """
        row = self.get_row_by_name(name)
        expect(row).to_be_visible(timeout=10000)
        switch = row.locator('.el-switch')
        switch.locator('.el-switch__core').click()
        # 处理切换后弹出的提示确认框
        confirm_btn = self.page.locator('.el-overlay-message-box button:has-text("确定")')
        if confirm_btn.is_visible(timeout=3000):
            confirm_btn.click()
            expect(confirm_btn).to_be_hidden(timeout=5000)
        return self

    def is_recommend_on_by_name(self, name: str) -> bool:
        """判断指定品牌的推荐开关是否为开启状态（is-checked）"""
        row = self.get_row_by_name(name)
        expect(row).to_be_visible(timeout=10000)
        switch = row.locator('.el-switch')
        return 'is-checked' in (switch.get_attribute('class') or '')

    def get_recommend_status_cell(self, name: str):
        """获取指定品牌的推荐状态单元格定位器"""
        row = self.get_row_by_name(name)
        return row.locator("td").nth(5)
