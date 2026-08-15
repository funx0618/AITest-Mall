"""
App Product Detail Page Object
页面：http://localhost:8060/#/pages/product/product?id=xxx
职责：商品详情页元素定位和基础交互
"""

from playwright.sync_api import Page, expect
from config.settings import WEB_BASE_URL


class AppProductPage:
    """App 商品详情页对象"""

    URL_TEMPLATE = WEB_BASE_URL + "/#/pages/product/product?id={product_id}"

    def __init__(self, page: Page):
        self.page = page

        # ========== 商品信息 ==========
        self.product_title = page.locator('[class*="product"] [class*="name"], [class*="goods"] [class*="name"]').first
        self.product_price = page.locator('[class*="price"]').first

        # ========== SKU 弹窗 ==========
        self.sku_popup = page.locator('[class*="sku"], [class*="popup--bottom"], .van-popup--bottom')
        self.sku_options = page.locator('[class*="sku"] [class*="item"], [class*="popup"] [class*="tag"]')

        # ========== 优惠券 ==========
        # exact=True 避免匹配到领取成功后残留的 toast 提示("领取优惠券成功！")
        self.claim_coupon_entry = page.get_by_text("领取优惠券", exact=True)
        self.coupon_popup = page.locator('[class*="coupon"]')
        self.claim_success_msg = page.get_by_text("领取优惠券成功")

        # ========== 操作按钮 ==========
        self.add_cart_btn = page.get_by_text("加入购物车")
        self.buy_now_btn = page.get_by_text("立即购买")
        self.confirm_btn = page.get_by_text("确定")

        # ========== 提示信息 ==========
        self.success_message = page.locator("text=操作成功")
        self.login_prompt = page.locator("text=你还没登录")

    # ========== 页面导航 ==========
    def goto_product(self, product_id: int):
        """导航到商品详情页"""
        url = self.URL_TEMPLATE.format(product_id=product_id)
        self.page.goto(url)
        # hash 路由下仅切换 query 不会触发页面组件重新加载数据，需强制刷新保证拿到目标商品的最新数据
        self.page.reload()
        return self

    # ========== 商品操作 ==========
    def add_to_cart(self):
        """点击加入购物车，在 SKU 弹窗中确认"""
        self.add_cart_btn.click()
        # 如果出现 SKU 弹窗，点击确定
        if self.confirm_btn.is_visible():
            self.confirm_btn.click()
        # 等待添加成功提示
        expect(self.success_message).to_be_visible(timeout=5000)
        return self

    def buy_now(self):
        """点击立即购买"""
        self.buy_now_btn.click()
        return self

    # ========== 优惠券操作 ==========
    def claim_coupon(self, coupon_name: str):
        """领取指定优惠券：打开优惠券弹窗 → 点击目标券 → 验证领取成功"""
        self.claim_coupon_entry.click()
        coupon_item = self.page.locator(f'text="{coupon_name}"').first
        expect(coupon_item).to_be_visible(timeout=10000)
        coupon_item.click()
        expect(self.claim_success_msg).to_be_visible(timeout=10000)
        return self

    def verify_coupon_not_visible(self, coupon_name: str):
        """验证优惠券不在弹窗列表中：打开优惠券弹窗 → 确认目标券不存在"""
        self.claim_coupon_entry.click()
        coupon_item = self.page.locator(f'text="{coupon_name}"')
        expect(coupon_item).to_have_count(0, timeout=5000)
        # 关闭弹窗
        self.page.keyboard.press("Escape")
        return self
