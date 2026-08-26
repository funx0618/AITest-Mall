"""
Admin Seckill Page Object
页面：秒杀活动列表页 / 秒杀时间段选择页 / 秒杀商品列表页
职责：只负责页面元素定位和基础交互，不包含业务逻辑
"""

from datetime import datetime, timezone, timedelta
from playwright.sync_api import Locator, Page, expect

# 上海时区（UTC+8），秒杀系统使用北京时间
SHANGHAI_TZ = timezone(timedelta(hours=8))


class FlashPage:
    """秒杀活动列表页面对象"""

    def __init__(self, page: Page):
        self.page = page

        # ========== 菜单导航 ==========
        self.hamburger = page.locator('svg.hamburger')
        self.menu_marketing = page.get_by_role('menuitem', name='营销')
        self.menu_flash_list = page.get_by_role('menu').get_by_role('link', name='秒杀活动列表')

        # ========== 搜索区域 ==========
        self.search_input = page.get_by_placeholder("活动名称")
        self.search_btn = page.get_by_role("button", name="查询搜索")
        self.reset_btn = page.get_by_role("button", name="重置")

        # ========== 数据列表区域 ==========
        self.add_btn = page.get_by_role("button", name="添加活动")
        self.data_table = page.locator("table").nth(1)

        # ========== 添加活动弹窗元素 ==========
        self.dialog_title = page.locator('.el-dialog:has-text("添加活动")')
        self.activity_title_input = self.dialog_title.get_by_role('textbox').first
        self.start_time_input = page.get_by_role('combobox', name='开始时间：')
        self.end_time_input = page.get_by_role('combobox', name='结束时间：')
        self.radio_online = self.dialog_title.locator('.el-radio:has-text("上线")')
        self.confirm_btn = self.dialog_title.get_by_role('button', name='确 定')
        self.cancel_btn = self.dialog_title.get_by_role('button', name='取 消')

    # ========== 页面导航 ==========
    def goto_list(self):
        """通过左侧菜单导航到秒杀活动列表页面（幂等）"""
        if self.search_input.is_visible():
            return self
        if not self.menu_marketing.is_visible():
            self.hamburger.click()
            expect(self.menu_marketing).to_be_visible()
        self.menu_marketing.click()
        self.menu_flash_list.click()
        expect(self.search_input).to_be_visible(timeout=15000)
        return self

    # ========== 搜索操作 ==========
    def search(self, keyword: str): 
        """输入活动名称并点击查询"""
        self.search_input.fill(keyword)
        self.search_btn.click()
        first_td = self.data_table.locator('tbody tr').first.locator('td').nth(2)
        empty_hint = self.page.locator('.el-table__empty-text').first
        expect(first_td.or_(empty_hint)).to_be_attached(timeout=10000)
        return self

    # ========== 表格数据 ==========
    def cell_contain_text(self, text: str):
        """获取包含指定文本的单元格"""
        return self.data_table.locator(f"tbody tr td:has-text('{text}')").first

    # ========== 添加活动操作 ==========
    def open_add_dialog(self):
        """点击添加活动按钮，等待弹窗出现"""
        self.add_btn.click()
        expect(self.activity_title_input).to_be_visible(timeout=5000)
        return self

    def fill_activity_title(self, title: str):
        """填写活动标题"""
        self.activity_title_input.clear()
        self.activity_title_input.fill(title)
        return self

    @staticmethod
    def select_date(page: Page, combobox: Locator, date_str: str):
        """通用方法：点击日期选择器并选择指定日期

        适用于 Element Plus DatePicker，后续优惠券、品牌等活动页面可直接复用。

        Args:
            page: Playwright Page 对象
            combobox: 日期选择器的 combobox 定位器
            date_str: 日期字符串，格式 "YYYY-MM-DD"，如 "2026-08-19"
        """
        combobox.click()
        picker = page.locator(
            ".el-picker__popper[aria-hidden='false']"
        ).last
        expect(picker).to_be_visible()
        # 通过填写输入框 + Enter 确认，避免在日历面板中逐格点击
        combobox.fill(date_str)
        page.keyboard.press('Enter')
        # 点击弹窗标题区域关闭日期选择面板（不能用 Escape，会关闭整个弹窗）
        page.locator('.el-dialog__title').click()
        page.wait_for_timeout(300)

    def set_start_time(self, date_str: str):
        """设置开始时间

        Args:
            date_str: 日期字符串，格式 "YYYY-MM-DD"
        """
        self.select_date(self.page, self.start_time_input, date_str)

    def set_end_time(self, date_str: str):
        """设置结束时间

        Args:
            date_str: 日期字符串，格式 "YYYY-MM-DD"
        """
        self.select_date(self.page, self.end_time_input, date_str)

    def select_online(self):
        """选择上线"""
        self.radio_online.click()
        return self

    def confirm_add(self):
        """点击确定按钮提交活动，处理可能弹出的提示消息框"""
        self.confirm_btn.click()
        # 处理可能弹出的提示消息框（如"添加成功"或校验提示）
        msg_box = self.page.locator('.el-overlay-message-box')
        if msg_box.is_visible(timeout=3000):
            msg_btn = msg_box.locator('button:has-text("确定")')
            if msg_btn.is_visible(timeout=1000):
                msg_btn.click()
                expect(msg_box).to_be_hidden(timeout=5000)
        # 等待页面回到列表状态
        expect(self.search_input).to_be_visible(timeout=15000)
        return self

    def click_set_product_by_name(self, activity_name: str):
        """根据活动名称找到对应行，点击设置商品按钮"""
        row = self.data_table.locator(
            f'tbody tr:has(td:has-text("{activity_name}"))'
        ).first
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("设置商品")').click()
        return self

    def click_session_list(self):
        """点击秒杀时间段列表按钮，进入时间段管理页面"""
        self.page.get_by_role('button', name='秒杀时间段列表').click()
        expect(self.page.get_by_role('button', name='添加')).to_be_visible(timeout=10000)
        return self

    def click_delete_by_name(self, activity_name: str):
        """根据活动名称找到对应行，点击删除按钮并确认"""
        row = self.data_table.locator(
            f'tbody tr:has(td:has-text("{activity_name}"))'
        ).first
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("删除")').click()
        confirm_btn = self.page.locator('.el-message-box__btns button:has-text("确定")')
        expect(confirm_btn).to_be_visible(timeout=5000)
        confirm_btn.click()
        expect(confirm_btn).to_be_hidden(timeout=5000)
        expect(row).to_be_hidden(timeout=10000)
        return self


class FlashSessionPage:
    """秒杀时间段选择页面对象"""

    def __init__(self, page: Page):
        self.page = page
        self.session_table = page.locator("table").nth(1)

        # ========== 添加时间段弹窗 ==========
        self.add_btn = page.get_by_role("button", name="添加")

    def get_current_session_name(self) -> str:
        """根据当前北京时间获取对应的秒杀时间段名称"""
        current_hour = datetime.now(SHANGHAI_TZ).hour
        print(f"Current hour: {current_hour}")
        if 8 <= current_hour < 10:
            return "8:00"
        elif 10 <= current_hour < 12:
            return "10:00"
        elif 12 <= current_hour < 14:
            return "12:00"
        elif 14 <= current_hour < 16:
            return "14:00"
        elif 16 <= current_hour < 18:
            return "16:00"
        elif 18 <= current_hour < 20:
            return "18:00"
        elif 20 <= current_hour < 22:
            return "20:00"
        else:
            return "8:00"

    def click_product_list(self, session_name: str = None):
        """点击指定时间段的商品列表按钮

        Args:
            session_name: 时间段名称，如 "8:00"、"14:00" 等。
                         若为 None 则使用当前时间段。
        """
        if session_name is None:
            session_name = self.get_current_session_name()
        row = self.session_table.locator('tbody tr').filter(
            has=self.page.get_by_text(session_name, exact=True)
        ).first
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("商品列表")').click()
        return self

    # ========== 添加时间段操作 ==========
    def open_add_dialog(self):
        """点击添加按钮，等待弹窗出现"""
        # 等待已有的消息提示消失，避免拦截点击
        toast = self.page.locator('.el-message')
        if toast.count() > 0:
            toast.first.wait_for(state='hidden', timeout=10000)
        self.add_btn.click()
        dialog = self.page.get_by_role("dialog", name="添加时间段")
        expect(dialog).to_be_visible(timeout=5000)
        return self

    def fill_session_name(self, name: str):
        """填写秒杀时间段名称"""
        self.page.get_by_role('textbox', name='秒杀时间段名称：').fill(name)
        return self

    def _select_time_value(self, time_str: str):
        """在已打开的时间面板中选择指定时间值

        Args:
            time_str: 时间字符串，格式 "HH:mm:ss"，如 "23:00:00"
        """
        hour, minute, second = time_str.split(":")
        panel = self.page.locator(".el-time-panel:visible")
        expect(panel).to_be_visible(timeout=5000)
        columns = panel.locator(".el-time-spinner__wrapper")

        def _click_spinner(col_index: int, value: str):
            """滚动 spinner 列到目标值并点击"""
            item = columns.nth(col_index).locator(
                ".el-time-spinner__item"
            ).filter(has_text=value)
            # 用 JS 滚动到目标项（Element Plus 用 transform 滚动）
            item.evaluate(
                "el => el.scrollIntoView({ block: 'center', behavior: 'instant' })"
            )
            item.click(force=True)

        # 小时列
        _click_spinner(0, hour)
        # 分钟列
        _click_spinner(1, minute)
        # 秒列
        _click_spinner(2, second)
        # 点击面板确定按钮
        panel.get_by_role("button", name="确定").click()
        expect(panel).to_be_hidden(timeout=5000)

    def set_session_start_time(self, time_str: str):
        """选择每日开始时间"""
        self.page.get_by_role('combobox', name='每日开始时间：').click()
        self._select_time_value(time_str)
        return self

    def set_session_end_time(self, time_str: str):
        """选择每日结束时间"""
        self.page.get_by_role('combobox', name='每日结束时间：').click()
        self._select_time_value(time_str)
        return self

    def confirm_add_session(self):
        """点击确定按钮，处理可能弹出的提示消息框"""
        self.page.get_by_role('button', name='确 定').click()
        msg_box = self.page.locator('.el-overlay-message-box')
        if msg_box.is_visible(timeout=3000):
            self.page.get_by_role('button', name='确定').click()
            expect(msg_box).to_be_hidden(timeout=5000)
        expect(self.session_table).to_be_visible(timeout=10000)
        return self

    def verify_session_visible(self, session_name: str):
        """验证时间段名称在表格中可见"""
        cell = self.session_table.locator('tbody tr td').filter(
            has=self.page.get_by_text(session_name, exact=True)
        ).first
        expect(cell).to_be_visible(timeout=10000)
        return self

    def verify_session_not_visible(self, session_name: str):
        """验证时间段名称在表格中不可见"""
        cell = self.session_table.locator('tbody tr td').filter(
            has=self.page.get_by_text(session_name, exact=True)
        )
        expect(cell).to_have_count(0, timeout=5000)
        return self

    def click_delete_session_by_name(self, session_name: str):
        """根据时间段名称找到对应行，点击删除按钮并确认"""
        row = self.session_table.locator('tbody tr').filter(
            has=self.page.get_by_text(session_name, exact=True)
        ).first
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("删除")').click()
        confirm_btn = self.page.locator('.el-message-box__btns button:has-text("确定")')
        expect(confirm_btn).to_be_visible(timeout=5000)
        confirm_btn.click()
        expect(confirm_btn).to_be_hidden(timeout=5000)
        expect(row).to_be_hidden(timeout=10000)
        return self


class FlashProductPage:
    """秒杀商品列表页面对象"""

    def __init__(self, page: Page):
        self.page = page
        self.add_btn = page.get_by_role("button", name="添加")
        self.product_table = page.locator("table").nth(1)

        # ========== 选择商品弹窗 ==========
        self.dialog = page.locator('.el-dialog:has-text("选择商品")')
        self.product_search_input = self.dialog.get_by_placeholder("商品名称搜索")
        # 通过输入框组件结构定位搜索按钮（无 accessible name）
        self.product_search_btn = self.product_search_input.locator(
            "xpath=ancestor::div[contains(@class, 'el-input-group')]"
        ).locator(".el-input-group__append button")
        self.product_rows = self.dialog.locator(
            "table.el-table__body tbody tr"
        )
        self.next_page_btn = self.dialog.get_by_role(
            "button", name="下一页"
        )
        self.dialog_confirm_btn = self.dialog.get_by_role(
            'button', name='确 定'
        )

    def open_add_product_dialog(self):
        """点击添加按钮，等待商品选择弹窗出现"""
        self.add_btn.click()
        expect(self.product_search_input).to_be_visible(timeout=5000)
        return self

    def find_product_in_current_page(self, product_name: str):
        """在当前分页查找商品"""
        return self.product_rows.filter(has_text=product_name).first

    def go_to_next_page(self):
        """进入下一页"""
        expect(self.next_page_btn).to_be_enabled(timeout=5000)
        self.next_page_btn.click()
        self.page.wait_for_timeout(300)

    def _dismiss_message_box(self, timeout: int = 3000):
        """处理 Element UI 弹出的提示消息框（如确认框、成功提示等）

        Args:
            timeout: 等待消息框出现的最大时间（毫秒）
        """
        msg_box = self.page.locator('.el-overlay-message-box')
        try:
            expect(msg_box).to_be_visible(timeout=timeout)
            msg_btn = msg_box.locator(
                '.el-message-box__btns button:has-text("确定")'
            )
            expect(msg_btn).to_be_visible(timeout=2000)
            msg_btn.click()
            expect(msg_box).to_be_hidden(timeout=5000)
        except Exception:
            pass  # 无消息框弹出，正常继续

    def search_and_select_product(self, product_name: str):
        """搜索并选择指定商品，支持分页遍历

        Args:
            product_name: 商品名称
        """
        # 1. 输入商品名称并点击搜索
        self.product_search_input.fill(product_name)
        self.product_search_btn.click()

        # 2. 处理搜索后可能弹出的提示弹窗
        self._dismiss_message_box()

        # 3. 遍历分页查找商品
        while True:
            row = self.find_product_in_current_page(product_name)
            if row.count() > 0:
                expect(row).to_be_visible(timeout=5000)
                row.locator('.el-checkbox__inner').click()
                return self

            # 当前页没有，检查下一页是否可用
            if self.next_page_btn.is_disabled():
                raise AssertionError(
                    f"商品不存在：{product_name}"
                )
            self.go_to_next_page()

    def confirm_select(self):
        """点击确定按钮，关闭商品选择弹窗"""
        self.dialog_confirm_btn.click()
        # 处理确定后可能弹出的提示弹窗
        self._dismiss_message_box()
        expect(self.dialog).to_be_hidden(timeout=10000)
        return self

    def has_product(self, product_name: str) -> bool:
        """检查商品列表中是否包含指定商品"""
        cell = self.product_table.locator(
            f'tbody tr td:has-text("{product_name}")'
        ).first
        return cell.is_visible()

    def click_edit_by_product_name(self, product_name: str):
        """根据商品名称找到对应行，点击编辑按钮"""
        row = self.product_table.locator(
            f'tbody tr:has(td:has-text("{product_name}"))'
        ).first
        expect(row).to_be_visible(timeout=10000)
        row.locator('button:has-text("编辑")').click()
        # 等待编辑弹窗出现
        expect(self.page.get_by_role('dialog')).to_be_visible(timeout=10000)
        return self

    def fill_flash_price(self, price: str):
        """填写秒杀价格"""
        price_input = self.page.get_by_role('dialog').locator(
            'label:has-text("秒杀价格")'
        ).locator('..').locator('input')
        expect(price_input).to_be_visible(timeout=5000)
        price_input.clear()
        price_input.fill(price)
        return self

    def submit_edit(self):
        """点击确定按钮，提交编辑"""
        confirm_btn = self.page.get_by_role('dialog').get_by_role(
            'button', name='确 定'
        )
        expect(confirm_btn).to_be_visible(timeout=5000)
        confirm_btn.click()
        # 处理确定后可能弹出的提示弹窗
        self._dismiss_message_box()
        return self
