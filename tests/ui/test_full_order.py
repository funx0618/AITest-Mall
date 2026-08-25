"""
下单流程测试用例（无折扣场景）
测试目标：App端 搜索商品 → 加入购物车 → 结算 → 验证实付款金额
"""

from playwright.sync_api import Page, expect
from ui.pages.app.app_home_page import AppHomePage
from ui.pages.app.app_product_page import AppProductPage
from ui.pages.app.app_cart_page import AppCartPage
from ui.pages.app.app_checkout_page import AppCheckoutPage
from ui.pages.app.app_order_page import AppMyOrderPage
from ui.pages.admin.admin_order_page import AdminOrderPage
from utils.data_loader import load_yaml

# 加载测试数据（文件名与测试文件对应）
test_data = load_yaml("ui/test_full_order.yaml")


class TestFullOrder:
    """下单流程测试（无折扣）"""

    def test_place_order_no_discount(self, app_logged_in: Page, admin_logged_in_page: Page):
        """无折扣商品下单流程：搜索 → 加购 → 结算 → 验证实付款 → admin发货"""
        data = test_data["test_place_order_no_discount"]
        product_name = data["product_name"]

        home = AppHomePage(app_logged_in)
        product = AppProductPage(app_logged_in)
        cart = AppCartPage(app_logged_in)
        checkout = AppCheckoutPage(app_logged_in)
        order_page = AppMyOrderPage(app_logged_in)

        # Step 1: 首页搜索商品
        home.search(product_name)
        home.click_product_by_name(product_name)

        # Step 2: 清空购物车，避免历史数据影响
        cart.goto()
        cart.clear_cart()

        # Step 3: 搜索商品，验证详情页标题，获取价格，加入购物车
        home.search(product_name)
        home.click_product_by_name(product_name)
        expect(product.product_title).to_be_visible()
        expect(product.product_title).to_have_text(product_name)
        unit_price = product.product_price.text_content()
        product.add_to_cart()

        # Step 4: 进入购物车，去结算
        cart.goto()
        cart.go_checkout()

        # Step 5: 结算页验证实付款金额与商品单价一致（无折扣场景）
        expect(checkout.submit_order_btn).to_be_visible(timeout=10000)
        pay_amount = app_logged_in.locator('[class*="price"], [class*="amount"]').last
        expect(pay_amount).to_be_visible(timeout=10000)
        expect(pay_amount).to_contain_text(unit_price)

        # Step 6: 提交订单并支付
        checkout.submit_order()
        checkout.select_wechat_pay()
        checkout.go_pay()

        # Step 7: 支付成功后，点击"查看订单"，验证订单状态为"待发货"
        app_logged_in.get_by_text("查看订单").click()
        expect(order_page.tab_all).to_be_visible(timeout=10000)

        # 在全部tab下，按商品名称+时间找到最新订单，验证状态为待发货
        latest_order = order_page.find_latest_order_by_product(product_name)
        order_page.verify_order_status(latest_order, "等待发货")

        # 点击订单进入详情页，验证详情页状态也是待发货，并获取订单编号和提交时间
        order_page.click_order_to_detail(latest_order)
        expect(order_page.waiting_delivery).to_be_visible(timeout=10000)
        order_sn = order_page.get_order_no_from_detail()
        submit_time = order_page.get_submit_time_from_detail()

        # Step 8: Admin后台根据订单编号搜索并发货
        admin_order = AdminOrderPage(admin_logged_in_page)
        admin_order.goto()
        admin_order.search_by_order_no(order_sn)
        admin_order.click_ship()
        admin_order.select_delivery("顺丰")
        admin_order.fill_tracking_no("SF1234567890")
        admin_order.confirm_ship()
        # 验证 admin 订单列表状态变为"已发货"
        admin_order.search_by_order_no(order_sn)
        admin_order.verify_order_status_shipped()

        # Step 9: Web App 我的 → 待收货，验证订单状态"等待收货"，确认收货
        app_logged_in.goto(AppHomePage.URL)
        order_page.go_to_my_page()
        order_page.click_tab("待收货")
        pending_order = order_page.find_order_by_time_and_product(submit_time, product_name)
        order_page.verify_order_status(pending_order, "等待收货")
        confirm_btn = pending_order.get_by_text("确认收货")
        expect(confirm_btn).to_be_visible(timeout=5000)
        confirm_btn.evaluate("el => { el.scrollIntoView({block: 'center'}); el.click(); }")
        # 弹窗确认
        app_logged_in.get_by_text("是否要确认收货").wait_for(timeout=5000)
        app_logged_in.get_by_text("确定", exact=True).last.click()

        # Step 10: 切换到"已完成"tab，验证订单存在
        order_page.click_tab("已完成")
        order_page.find_order_by_time_and_product(submit_time, product_name)
