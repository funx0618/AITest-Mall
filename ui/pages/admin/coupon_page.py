"""
Admin Coupon Page Object
页面：http://localhost:8090/#/sms/coupon
职责：只负责页面元素定位和基础交互，不包含业务逻辑
"""

from datetime import date, timedelta
from playwright.sync_api import Page, expect


class CouponPage:
    """优惠券列表页面对象"""

    def __init__(self, page: Page):
        self.page = page

        # ========== 菜单导航 ==========
        self.hamburger = page.locator('svg.hamburger')
        self.menu_marketing = page.get_by_role('menuitem', name='营销')
        self.menu_coupon_list = page.get_by_role('menu').get_by_role('link', name='优惠券列表')

        # ========== 搜索区域 ==========
        self.search_input = page.get_by_placeholder("优惠券名称")
        self.search_btn = page.get_by_role("button", name="查询搜索")
        self.reset_btn = page.get_by_role("button", name="重置")

        # ========== 数据列表区域 ==========
        self.add_btn = page.get_by_role("button", name="添加")
        self.coupon_table = page.locator("table").nth(1)  # 第二个table是数据表
        self.table_cells = self.coupon_table.locator("tbody tr td")

        # ========== 添加优惠券页面元素 ==========
        # 优惠券类型
        self.coupon_type_select = page.locator('.el-form-item:has-text("优惠券类型") .el-select')
        # 优惠券名称
        self.coupon_name_input = page.get_by_role('textbox', name='* 优惠券名称：')
        # 适用平台
        self.platform_select = page.locator('.el-form-item:has-text("适用平台") .el-select')
        # 总发行量
        self.total_input = page.get_by_role('textbox', name='* 总发行量：')
        # 面额
        self.amount_input = page.locator('.el-form-item:has-text("面额") input[type="text"]').first
        # 使用门槛
        self.threshold_input = page.get_by_role('textbox', name='* 使用门槛：')
        # 领取日期
        self.claim_date_input = page.locator('.el-form-item:has-text("领取日期") .el-date-editor input')
        # 有效期 - 开始日期
        self.validity_start_input = page.locator('.el-form-item:has-text("有效期") .el-date-editor').first.locator('input')
        # 有效期 - 结束日期
        self.validity_end_input = page.locator('.el-form-item:has-text("有效期") .el-date-editor').last.locator('input')
        # 可使用商品 - 指定商品
        self.radio_specified_product = page.locator('.el-radio-button:has-text("指定商品")')
        # 指定商品搜索框
        self.product_search_input = page.locator('.el-select:has-text("商品名称/商品货号") input')
        # 添加商品按钮
        self.add_product_btn = page.get_by_role('button', name='添加')
        # 提交按钮
        self.submit_btn = page.get_by_role('button', name='提交')
        # 重置按钮（添加页面）
        self.form_reset_btn = page.get_by_role('button', name='重置')

        # ========== 表格列头 ==========
        self.col_id = page.get_by_role("columnheader", name="编号")
        self.col_name = page.get_by_role("columnheader", name="优惠劵名称")
        self.col_type = page.get_by_role("columnheader", name="优惠券类型")
        self.col_product = page.get_by_role("columnheader", name="可使用商品")
        self.col_threshold = page.get_by_role("columnheader", name="使用门槛")
        self.col_amount = page.get_by_role("columnheader", name="面值")
        self.col_platform = page.get_by_role("columnheader", name="适用平台")
        self.col_validity = page.get_by_role("columnheader", name="有效期")
        self.col_status = page.get_by_role("columnheader", name="状态")
        self.col_action = page.get_by_role("columnheader", name="操作")

    # ========== 页面导航 ==========
    def goto_list(self):
        """通过左侧菜单导航到优惠券列表页面（幂等）"""
        if self.search_input.is_visible():
            return self
        if not self.menu_marketing.is_visible():
            self.hamburger.click()
            expect(self.menu_marketing).to_be_visible()
        self.menu_marketing.click()
        self.menu_coupon_list.click()
        expect(self.search_input).to_be_visible(timeout=15000)
        return self

    def goto_add(self):
        """导航到添加优惠券页面"""
        self.goto_list()
        self.add_btn.click()
        expect(self.coupon_name_input).to_be_visible(timeout=15000)
        return self

    # ========== 搜索操作 ==========
    def search(self, keyword: str):
        """输入优惠券名称并点击查询"""
        self.search_input.fill(keyword)
        self.search_btn.click()
        first_td = self.coupon_table.locator('tbody tr').first.locator('td').nth(4)
        empty_hint = self.page.locator('.el-table__empty-text').first
        expect(first_td.or_(empty_hint)).to_be_attached(timeout=10000)
        return self

    def reset(self):
        """点击重置按钮"""
        self.reset_btn.click()
        expect(self.search_btn).to_be_enabled(timeout=5000)
        return self

    # ========== 表格数据 ==========
    def has_data(self):
        """判断表格是否有数据"""
        return self.table_cells.first

    def cell_contain_text(self, text: str):
        """获取包含指定文本的单元格"""
        return self.coupon_table.locator(f"tbody tr td:has-text('{text}')").first

    # ========== 添加优惠券表单操作 ==========
    def fill_name(self, name: str):
        """填写优惠券名称"""
        self.coupon_name_input.clear()
        self.coupon_name_input.fill(name)
        return self

    def select_platform(self, platform: str = "全平台"):
        """选择适用平台"""
        self.platform_select.click()
        self.page.locator(f'.el-select-dropdown .el-select-dropdown__item:has-text("{platform}")').click()
        return self

    def fill_total(self, total: str):
        """填写总发行量"""
        self.total_input.clear()
        self.total_input.fill(total)
        return self

    def fill_amount(self, amount: str):
        """填写面额"""
        self.amount_input.clear()
        self.amount_input.fill(amount)
        return self

    def fill_threshold(self, threshold: str):
        """填写使用门槛"""
        self.threshold_input.clear()
        self.threshold_input.fill(threshold)
        return self

    def set_claim_date_today(self):
        """设置领取日期为今天，通过直接输入日期"""
        today = date.today().strftime("%Y-%m-%d")
        self.claim_date_input.click()
        self.claim_date_input.fill(today)
        self.page.keyboard.press('Enter')
        self.page.keyboard.press('Escape')
        return self

    def set_validity_range(self, start_date: date, end_date: date):
        """设置有效期范围"""
        # 开始日期
        self.validity_start_input.click()
        self.validity_start_input.fill(start_date.strftime("%Y-%m-%d"))
        self.page.keyboard.press('Enter')

        # 结束日期
        self.validity_end_input.click()
        self.validity_end_input.fill(end_date.strftime("%Y-%m-%d"))
        self.page.keyboard.press('Enter')
        self.page.keyboard.press('Escape')
        return self

    def set_validity_days(self, days_before: int = 30, days_after: int = 30):
        """设置有效期为今天前后 N 天，通过直接输入日期"""
        today = date.today()
        start = today - timedelta(days=days_before)
        end = today + timedelta(days=days_after)
        return self.set_validity_range(start, end)

    def select_specified_product(self):
        """选择"指定商品"单选按钮"""
        self.radio_specified_product.click()
        return self

    def search_and_add_product(self, product_name: str):
        """搜索并添加指定商品"""
        # 等待商品搜索框出现
        expect(self.product_search_input).to_be_visible(timeout=5000)
        self.product_search_input.fill(product_name)
        # 等待下拉选项出现并点击匹配项
        option = self.page.locator(
            f'.el-select-dropdown__item:has-text("{product_name}")'
        ).first
        expect(option).to_be_visible(timeout=10000)
        option.click()
        # 点击添加按钮
        self.add_product_btn.click()
        return self

    def submit(self):
        """点击提交按钮，并确认弹窗"""
        self.submit_btn.click()
        # 确认"是否提交数据"弹窗
        confirm_dialog = self.page.locator('.el-message-box__btns button:has-text("确定")')
        expect(confirm_dialog).to_be_visible(timeout=5000)
        confirm_dialog.click()
        # 等待页面跳转回列表页
        expect(self.search_input).to_be_visible(timeout=15000)
        return self

    # ========== 删除操作 ==========
    def click_delete_by_name(self, coupon_name: str):
        """根据优惠券名称找到对应行，点击删除按钮并确认，等待该行消失"""
        row = self.coupon_table.locator(
            f'tbody tr:has(td:nth-child(3):has-text("{coupon_name}"))'
        ).first
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("删除")').click()
        # 等待确认弹窗出现
        confirm_btn = self.page.locator('.el-message-box__btns button:has-text("确定")')
        expect(confirm_btn).to_be_visible(timeout=5000)
        confirm_btn.click()
        # 等待弹窗关闭
        expect(confirm_btn).to_be_hidden(timeout=5000)
        # 等待该行从表格中消失
        expect(row).to_be_hidden(timeout=10000)
        return self


