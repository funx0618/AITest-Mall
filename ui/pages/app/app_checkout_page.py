"""
App Checkout / Payment Page Object
页面：结算页、支付页
职责：结算和支付流程的元素定位和基础交互
"""

from playwright.sync_api import Page, expect


class AppCheckoutPage:
    """App 结算/支付页面对象"""

    def __init__(self, page: Page):
        self.page = page

        # ========== 结算页（createOrder）元素 ==========
        self.address_link = page.locator('a[href*="address"], [class*="address"]').first
        self.submit_order_btn = page.get_by_text("提交订单")

        # ========== 提交成功弹窗 ==========
        self.dialog_go_pay = page.get_by_text("去支付")
        self.dialog_cancel = page.get_by_text("取消")

        # ========== 支付页元素 ==========
        self.wechat_pay = page.get_by_text("微信支付")
        self.confirm_pay_btn = page.get_by_text("确认支付")

        # ========== 地址列表页元素 ==========
        self.default_tag = page.locator("text=默认")

    # ========== 结算操作 ==========
    def select_default_address(self):
        """在结算页选择默认收货地址"""
        self.address_link.click()
        expect(self.page.locator("text=收货地址")).to_be_visible(timeout=5000)
        self.default_tag.click()
        expect(self.submit_order_btn).to_be_visible(timeout=5000)
        return self

    def submit_order(self):
        """提交订单，并在弹窗中点击去支付"""
        self.submit_order_btn.click()
        # 等待"订单创建成功"弹窗出现，点击"去支付"
        expect(self.dialog_go_pay).to_be_visible(timeout=10000)
        self.dialog_go_pay.click()
        return self

    def select_wechat_pay(self):
        """在支付页选择微信支付"""
        expect(self.wechat_pay).to_be_visible(timeout=10000)
        self.wechat_pay.click()
        return self

    def go_pay(self):
        """点击确认支付"""
        expect(self.confirm_pay_btn).to_be_visible(timeout=10000)
        self.confirm_pay_btn.click()
        return self
