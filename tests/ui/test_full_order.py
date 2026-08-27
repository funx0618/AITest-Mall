"""
下单流程测试用例（无折扣场景）
测试目标：App端 搜索商品 → 加入购物车 → 结算 → 验证实付款金额
"""

from playwright.sync_api import Page, expect
from playwright._impl._errors import TimeoutError as PlaywrightTimeout
from ui.pages.app.app_home_page import AppHomePage
from ui.pages.app.app_product_page import AppProductPage
from ui.pages.app.app_cart_page import AppCartPage
from ui.pages.app.app_checkout_page import AppCheckoutPage
from ui.pages.app.app_order_page import AppMyOrderPage
from ui.pages.admin.admin_order_page import AdminOrderPage
from ui.flows.app.app_order_flow import AppOrderFlow
from ui.flows.admin.flash_flow import FlashFlow
from ui.flows.admin.coupon_flow import CouponFlow
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

        # 在全部tab下，按商品名称找到最新订单，验证状态为待发货
        latest_order = order_page.find_latest_order_by_product(product_name)
        order_page.verify_order_status(latest_order, "等待发货")
        # 从列表项直接获取提交时间，避免再去详情页获取
        submit_time = latest_order.locator(".time").inner_text().strip()

        # 点击订单进入详情页，验证详情页状态也是待发货，并获取订单编号
        order_page.click_order_to_detail(latest_order)
        expect(order_page.waiting_delivery).to_be_visible(timeout=10000)
        order_sn = order_page.get_order_no_from_detail()

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

        # Step 9: Web App 待收货，确认收货
        app_flow = AppOrderFlow(app_logged_in)
        app_flow.confirm_pending_receipt(submit_time, product_name)

        # Step 10: 切换到"已完成"tab，验证订单存在
        order_page.click_tab("已完成")
        order_page.find_order_by_time_and_product(submit_time, product_name)

    def test_coupon_flash_order(self, app_logged_in: Page, admin_logged_in_page: Page):
        """使用优惠券的秒杀下单流程：新增优惠券 → 新增秒杀活动 → 设置商品 → 编辑秒杀价格 → App秒杀专区下单 → 验证实付款

        注意：秒杀后的价格必须大于优惠券的使用门槛，否则秒杀和优惠券不能同时使用。
        """
        data = test_data["test_coupon_flash_order"]
        coupon_name = data["coupon_name"]
        activity_title = data["activity_title"]
        product_name = data["product_name"]
        flash_price = data["flash_price"]

        # ========== Admin 端：新增优惠券 ==========
        coupon_flow = CouponFlow(admin_logged_in_page)
        coupon_flow.add_coupon(
            name=data["coupon_name"],
            platform=data["platform"],
            total=data["total"],
            amount=data["coupon_amount"],
            threshold=data["threshold"],
        )
        # 搜索验证新增优惠券已创建
        coupon_flow.coupon_page.goto_list()
        coupon_flow.coupon_page.search(coupon_name)
        expect(coupon_flow.coupon_page.cell_contain_text(coupon_name)).to_be_visible()

        # ========== Admin 端：新增秒杀活动 ==========
        flash_flow = FlashFlow(admin_logged_in_page)
        flash_flow.add_flash_sale(title=activity_title)
        # 搜索验证新增秒杀活动已创建
        flash_flow.flash_page.goto_list()
        flash_flow.flash_page.search(activity_title)
        expect(flash_flow.flash_page.cell_contain_text(activity_title)).to_be_visible()

        # ========== Admin 端：设置秒杀商品 ==========
        flash_flow.set_flash_product(
            activity_name=activity_title,
            product_name=product_name,
        )

        # ========== Admin 端：编辑秒杀价格为 2400 ==========
        flash_flow.edit_flash_product_price(
            activity_name=activity_title,
            product_name=product_name,
            flash_price=flash_price,
        )

        # ========== App 端 + 清理（try/finally 确保清理一定执行） ==========
        try:
            home = AppHomePage(app_logged_in)
            product = AppProductPage(app_logged_in)
            cart = AppCartPage(app_logged_in)
            checkout = AppCheckoutPage(app_logged_in)
            order_page = AppMyOrderPage(app_logged_in)

            # Step 1: 清空购物车，避免历史数据影响
            cart.goto()
            cart.clear_cart()

            # Step 2: 在秒杀专区点击商品，进入商品详情
            home.goto()
            home.click_flash_sale_product(product_name)
            expect(product.product_title).to_be_visible(timeout=10000)

            # Step 3: 在商品详情页领取优惠券（已领取过也可以继续）
            try:
                product.claim_coupon(coupon_name)
            except (PlaywrightTimeout, AssertionError):
                product.verify_already_claimed(coupon_name)

            # Step 4: 加入购物车
            product.add_to_cart()

            # Step 5: 进入购物车，去结算
            cart.goto()
            cart.go_checkout()

            # Step 6: 结算页选择优惠券，验证优惠金额和实付款
            expect(checkout.submit_order_btn).to_be_visible(timeout=10000)
            checkout.select_coupon(coupon_name)

            # 验证活动优惠 = 原价 - 秒杀价
            original_price = int(data["original_price"])
            expected_activity_discount = str(original_price - int(flash_price))
            activity_discount_text = checkout.get_discount_amount("活动优惠")
            assert expected_activity_discount in activity_discount_text

            # 验证优惠券面额
            coupon_discount_text = checkout.get_discount_amount("优惠券")
            assert data["coupon_amount"] in coupon_discount_text

            # 验证实付款 = 秒杀价 - 优惠券面额
            expected_pay = str(int(flash_price) - int(data["coupon_amount"]))
            actual_pay_text = checkout.get_actual_pay_amount()
            assert expected_pay in actual_pay_text

            # Step 7: 提交订单并支付
            checkout.submit_order()
            checkout.select_wechat_pay()
            checkout.go_pay()

            # Step 8: 支付成功后，点击"查看订单"，验证订单状态为"待发货"
            app_logged_in.get_by_text("查看订单").click()
            expect(order_page.tab_all).to_be_visible(timeout=10000)
            latest_order = order_page.find_latest_order_by_product(product_name)
            order_page.verify_order_status(latest_order, "等待发货")

        finally:
            # ========== 清理数据：删除秒杀活动和优惠券 ==========
            admin_logged_in_page.reload()
            flash_flow.delete_flash_sale(activity_title)
            coupon_flow.delete_coupon(coupon_name)

    def test_coupon_order(self, app_logged_in: Page, admin_logged_in_page: Page):
        """使用优惠券下单流程（无秒杀）：新增优惠券 → App搜索商品领取优惠券 → 加购 → 结算选择优惠券 → 验证实付款

        实付款 = 商品原价 - 优惠券面额
        """
        data = test_data["test_coupon_order"]
        coupon_name = data["coupon_name"]
        product_name = data["product_name"]

        # ========== Admin 端：新增优惠券 ==========
        coupon_flow = CouponFlow(admin_logged_in_page)
        coupon_flow.add_coupon(
            name=coupon_name,
            platform=data["platform"],
            total=data["total"],
            amount=data["coupon_amount"],
            threshold=data["threshold"],
        )
        # 搜索验证新增优惠券已创建
        coupon_flow.coupon_page.goto_list()
        coupon_flow.coupon_page.search(coupon_name)
        expect(coupon_flow.coupon_page.cell_contain_text(coupon_name)).to_be_visible()

        # ========== App 端 + 清理（try/finally 确保清理一定执行） ==========
        try:
            home = AppHomePage(app_logged_in)
            product = AppProductPage(app_logged_in)
            cart = AppCartPage(app_logged_in)
            checkout = AppCheckoutPage(app_logged_in)
            order_page = AppMyOrderPage(app_logged_in)

            # Step 1: 清空购物车，避免历史数据影响
            cart.goto()
            cart.clear_cart()

            # Step 2: 搜索商品，进入详情页
            home.search(product_name)
            home.click_product_by_name(product_name)
            expect(product.product_title).to_be_visible()
            expect(product.product_title).to_have_text(product_name)
            unit_price = product.product_price.text_content()

            # Step 3: 领取优惠券（已领取过也可以继续）
            try:
                product.claim_coupon(coupon_name)
            except (PlaywrightTimeout, AssertionError):
                product.verify_already_claimed(coupon_name)

            # Step 4: 加入购物车
            product.add_to_cart()

            # Step 5: 进入购物车，去结算
            cart.goto()
            cart.go_checkout()

            # Step 6: 结算页选择优惠券，验证优惠金额和实付款
            expect(checkout.submit_order_btn).to_be_visible(timeout=10000)
            checkout.select_coupon(coupon_name)

            # 验证优惠券面额
            coupon_discount_text = checkout.get_discount_amount("优惠券")
            assert data["coupon_amount"] in coupon_discount_text

            # 验证实付款 = 商品原价 - 优惠券面额
            expected_pay = str(int(data["original_price"]) - int(data["coupon_amount"]))
            actual_pay_text = checkout.get_actual_pay_amount()
            assert expected_pay in actual_pay_text

            # Step 7: 提交订单并支付
            checkout.submit_order()
            checkout.select_wechat_pay()
            checkout.go_pay()

            # Step 8: 支付成功后，点击"查看订单"，验证订单状态为"待发货"
            app_logged_in.get_by_text("查看订单").click()
            expect(order_page.tab_all).to_be_visible(timeout=10000)
            latest_order = order_page.find_latest_order_by_product(product_name)
            order_page.verify_order_status(latest_order, "等待发货")

        finally:
            # ========== 清理数据：删除优惠券 ==========
            admin_logged_in_page.reload()
            coupon_flow.delete_coupon(coupon_name)

