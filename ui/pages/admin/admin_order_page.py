"""
Admin Order Page Object
页面：http://localhost:8090/#/oms/order
职责：后台订单列表页面元素定位和基础交互
"""

from playwright.sync_api import Page, expect


class AdminOrderPage:
    """后台订单列表页面对象"""

    def __init__(self, page: Page):
        self.page = page

        # ========== 菜单导航 ==========
        self.menu_order = page.get_by_role("menuitem", name="订单")
        self.menu_order_list = page.get_by_role("link", name="订单列表")

        # ========== 搜索区域 ==========
        self.search_input = page.get_by_placeholder("订单编号")
        self.search_btn = page.get_by_role("button", name="查询搜索")

        # ========== 数据列表 ==========
        self.order_table = page.locator("table").nth(1)
        self.table_cells = self.order_table.locator("tbody tr td")

        # ========== 发货页面（非弹窗）==========
        self.ship_confirm_btn = page.locator('button:has-text("确定")').last
        self.sf_option = page.locator('.el-select-dropdown__item:has-text("顺丰"), [class*="option"]:has-text("顺丰")')

    # ========== 页面导航 ==========
    def goto(self):
        """通过左侧菜单导航到订单列表页面"""
        self.menu_order.click()
        self.menu_order_list.click()
        expect(self.search_input).to_be_visible(timeout=15000)
        return self

    # ========== 搜索操作 ==========
    def search_by_order_no(self, order_no: str):
        """按订单编号搜索"""
        self.search_input.fill(order_no)
        self.search_btn.click()
        expect(self.search_btn).to_be_enabled(timeout=5000)
        # 等待表格数据刷新完成
        expect(self.order_table.locator("tbody tr").first).to_be_visible(timeout=10000)
        return self

    # ========== 发货操作 ==========
    def click_ship(self):
        """点击订单发货按钮，进入发货列表页面"""
        ship_btn = self.order_table.locator('button:has-text("订单发货"), a:has-text("订单发货")')
        expect(ship_btn).to_be_visible(timeout=10000)
        ship_btn.click()
        # 等待发货列表页面加载
        expect(self.page.get_by_text("发货列表")).to_be_visible(timeout=10000)
        return self

    def select_delivery(self, company: str = "顺丰"):
        """选择快递公司

        Args:
            company: 快递公司名称，如 "顺丰快递"、"圆通快递"、"中通快递" 等
        """
        # 点击表格中的下拉选择框
        self.page.locator('table .el-select').first.click()
        # 等待下拉面板出现，点击对应快递公司选项
        dropdown_panel = self.page.locator('.el-select-dropdown')
        expect(dropdown_panel).to_be_visible(timeout=5000)
        self.page.locator(f'.el-select-dropdown__item:has-text("{company}")').click(timeout=10000)
        return self

    def fill_tracking_no(self, tracking_no: str):
        """填写物流单号"""
        tracking_input = self.page.locator('table .el-input__inner').last
        tracking_input.fill(tracking_no)
        return self

    def confirm_ship(self):
        """确认发货：先点页面确定，再点弹窗确定，等待返回订单列表"""
        # 第一次点击：提交发货表单
        self.page.locator('button:has-text("确定")').first.click()
        # 等待确认弹窗出现（dialog role="dialog"）
        confirm_dialog = self.page.get_by_role("dialog")
        expect(confirm_dialog).to_be_visible(timeout=5000)
        # 第二次点击：确认弹窗中的确定
        confirm_dialog.locator('button:has-text("确定")').click()
        # 等待发货完成，页面回到订单列表
        expect(self.search_input).to_be_visible(timeout=10000)
        return self
