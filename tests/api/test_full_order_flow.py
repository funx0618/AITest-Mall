"""
端到端全流程测试（API 层）
职责：验证跨 App + Admin 的完整业务闭环
覆盖范围：
  - App: 登录 → 加购物车 → 确认订单 → 提交订单 → 支付
  - Admin: 查询订单 → 发货
  - App: 确认收货 → 完成
涉及表：oms_cart_item, oms_order, oms_order_item
"""

import random
import pytest
from playwright.sync_api import Playwright
from config.settings import APP_API_BASE_URL, ADMIN_API_BASE_URL
from api.app.cart_service import AppCartService
from api.app.coupon_service import AppCouponService
from api.app.order_service import AppOrderService
from api.admin.order_service import AdminOrderService
from utils.db.db_client import DBClient
from utils.data_loader import load_yaml


# ==================== Fixtures ====================


@pytest.fixture
def app_cart_service(playwright: Playwright, app_token: str):
    """已认证的 AppCartService 实例"""
    api_context = playwright.request.new_context(base_url=APP_API_BASE_URL)
    yield AppCartService(api_context, app_token)
    api_context.dispose()


@pytest.fixture
def app_coupon_service(playwright: Playwright, app_token: str):
    """已认证的 AppCouponService 实例"""
    api_context = playwright.request.new_context(base_url=APP_API_BASE_URL)
    yield AppCouponService(api_context, app_token)
    api_context.dispose()


@pytest.fixture
def app_order_service(playwright: Playwright, app_token: str):
    """已认证的 AppOrderService 实例"""
    api_context = playwright.request.new_context(base_url=APP_API_BASE_URL)
    yield AppOrderService(api_context, app_token)
    api_context.dispose()


@pytest.fixture
def admin_order_service(playwright: Playwright, admin_token: str):
    """已认证的 AdminOrderService 实例"""
    api_context = playwright.request.new_context(base_url=ADMIN_API_BASE_URL)
    yield AdminOrderService(api_context, admin_token)
    api_context.dispose()


@pytest.fixture
def test_data(request):
    """根据测试方法名自动加载对应测试数据"""
    data = load_yaml("api/test_full_order_flow.yaml")
    return data[request.function.__name__]


# ==================== 测试类 ====================


class TestFullOrderFlow:
    """跨 App + Admin 全流程订单测试"""

    def test_full_order_flow_no_discount(
        self,
        app_cart_service: AppCartService,
        app_order_service: AppOrderService,
        admin_order_service: AdminOrderService,
        db: DBClient,
        test_data: dict,
    ):
        """完整下单流程：加购 → 确认单 → 提交订单 → 支付宝支付 → 后台发货 → 确认收货"""
        product_id = test_data["product_id"]
        product_sku_id = test_data["sku_id"]
        quantity = test_data["quantity"]

        # ==================== 1. 准备：验证商品、查询收货地址 ====================
        product_row = db.query(
            "SELECT id, price, name, promotion_type FROM pms_product "
            "WHERE id = %s AND publish_status = 1 AND delete_status = 0",
            (product_id,),
        )
        assert len(product_row) > 0, f"未找到上架商品: id={product_id}"
        expected_promotion_type = test_data.get("promotion_type", 0)
        assert product_row[0]["promotion_type"] == expected_promotion_type, \
            f"商品 promotion_type 不匹配: 期望 {expected_promotion_type}, " \
            f"实际 {product_row[0]['promotion_type']}"

        sku_row = db.query(
            "SELECT id, price, promotion_price FROM pms_sku_stock "
            "WHERE id = %s AND product_id = %s",
            (product_sku_id, product_id),
        )
        assert len(sku_row) > 0, f"商品(ID={product_id})无 SKU(ID={product_sku_id})数据"
        sku_price = float(sku_row[0]["price"])

        address_row = db.query(
            "SELECT id FROM ums_member_receive_address "
            "WHERE member_id = 12 AND default_status = 1 LIMIT 1"
        )
        assert len(address_row) > 0, "数据库中无默认收货地址"
        address_id = address_row[0]["id"]

        # ==================== 2. 清理购物车并加购 ====================
        db.query(
            "UPDATE oms_cart_item SET delete_status = 1 "
            "WHERE product_id = %s AND product_sku_id = %s AND delete_status = 0",
            (product_id, product_sku_id),
        )

        resp = app_cart_service.add_cart(product_id, product_sku_id, quantity)
        assert resp.ok, f"加购请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"加购失败: {resp.json}"

        cart_row = db.query(
            "SELECT id, quantity FROM oms_cart_item "
            "WHERE product_id = %s AND product_sku_id = %s AND delete_status = 0",
            (product_id, product_sku_id),
        )
        assert len(cart_row) > 0, "加购后数据库中未找到购物车记录"
        cart_ids = [cart_row[0]["id"]]
        cart_quantity = int(cart_row[0]["quantity"])

        # ==================== 3. 生成确认单 — 从响应中获取期望金额 ====================
        resp = app_order_service.generate_confirm_order(cart_ids)
        assert resp.ok, f"生成确认单请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"生成确认单失败: {resp.json}"

        calc_amount = resp.data["calcAmount"]
        expected_total = float(calc_amount["totalAmount"])
        expected_freight = float(calc_amount["freightAmount"])
        expected_promotion = float(calc_amount["promotionAmount"])
        expected_integration = float(calc_amount.get("integrationAmount", 0))

        # 验证金额一致性
        assert expected_total == cart_quantity * sku_price, \
            f"确认单商品合计不匹配: 期望 {cart_quantity * sku_price}, 实际 {expected_total}"

        expected_pay = expected_total + expected_freight - expected_promotion - expected_integration

        # ==================== 4. 提交订单 — 验证金额 ====================
        order_param = {
            "payType": test_data["pay_type"],
            "cartIds": cart_ids,
            "memberReceiveAddressId": address_id,
            "useIntegration": test_data["use_integration"],
        }
        resp = app_order_service.generate_order(order_param)
        assert resp.ok, f"提交订单请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"提交订单失败: {resp.json}"
        order_id = resp.data["order"]["id"]
        assert order_id, f"提交订单未返回订单ID: {resp.json}"

        order_data = resp.data["order"]
        assert float(order_data["payAmount"]) == expected_pay, \
            f"订单实付款不匹配: 期望 {expected_pay}, 实际 {order_data['payAmount']}"

        # 验证数据库订单记录
        order_row = db.query("SELECT * FROM oms_order WHERE id = %s", (order_id,))
        assert len(order_row) > 0, f"数据库中未找到订单: id={order_id}"
        order = order_row[0]
        assert order["status"] == 0, f"订单状态应为待付款(0)，实际: {order['status']}"
        assert float(order["total_amount"]) == expected_total, \
            f"DB订单商品合计不匹配: 期望 {expected_total}, 实际 {order['total_amount']}"
        assert float(order["pay_amount"]) == expected_pay, \
            f"DB订单实付款不匹配: 期望 {expected_pay}, 实际 {order['pay_amount']}"
        assert float(order["promotion_amount"]) == expected_promotion, \
            f"DB订单活动优惠不匹配: 期望 {expected_promotion}, 实际 {order['promotion_amount']}"


        # 验证订单明细
        item_rows = db.query(
            "SELECT * FROM oms_order_item WHERE order_id = %s", (order_id,)
        )
        assert len(item_rows) > 0, f"数据库中未找到订单明细: order_id={order_id}"
        assert item_rows[0]["product_id"] == product_id, \
            f"订单明细商品ID不匹配: 期望 {product_id}, 实际 {item_rows[0]['product_id']}"

        # ==================== 5. 模拟支付（调用 paySuccess A。PI） ====================
        resp = app_order_service.pay_success(order_id, test_data["pay_type"])
        assert resp.ok, f"支付请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"支付失败: {resp.json}"

        # 验证订单状态变为待发货(1)
        order_after_pay = db.query("SELECT status FROM oms_order WHERE id = %s", (order_id,))
        assert order_after_pay[0]["status"] == 1, \
            f"支付后订单状态应为待发货(1)，实际: {order_after_pay[0]['status']}"

        # ==================== 6. 后台发货 ====================
        delivery_company = test_data["delivery_company"]
        delivery_prefix = test_data["delivery_prefix"]
        tracking_no = f"{delivery_prefix}{random.randint(1000000000, 9999999999)}"

        delivery_param = [{
            "orderId": order_id,
            "deliveryCompany": delivery_company,
            "deliverySn": tracking_no,
        }]
        resp = admin_order_service.update_delivery(delivery_param)
        assert resp.ok, f"发货请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"发货失败: {resp.json}"

        # 验证订单状态变为已发货(2)
        order_after_ship = db.query(
            "SELECT status, delivery_company, delivery_sn FROM oms_order WHERE id = %s",
            (order_id,),
        )
        assert order_after_ship[0]["status"] == 2, \
            f"发货后订单状态应为已发货(2)，实际: {order_after_ship[0]['status']}"
        assert order_after_ship[0]["delivery_company"] == delivery_company, \
            f"物流公司不匹配: 期望 {delivery_company}, 实际 {order_after_ship[0]['delivery_company']}"
        assert order_after_ship[0]["delivery_sn"] == tracking_no, \
            f"物流单号不匹配: 期望 {tracking_no}, 实际 {order_after_ship[0]['delivery_sn']}"

        # ==================== 7. 确认收货 ====================
        resp = app_order_service.confirm_receive_order(order_id)
        assert resp.ok, f"确认收货请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"确认收货失败: {resp.json}"

        # 验证订单状态变为已完成(3)
        order_final = db.query("SELECT status FROM oms_order WHERE id = %s", (order_id,))
        assert order_final[0]["status"] == 3, \
            f"确认收货后订单状态应为已完成(3)，实际: {order_final[0]['status']}"


