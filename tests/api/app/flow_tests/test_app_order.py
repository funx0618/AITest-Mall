"""
订单流程测试 — 加购 → 确认单 → 提交订单 → 取消订单
职责：验证前台商城完整下单+取消流程
对应 API 文档：docs/api docs/app-api.md — OmsPortalOrderController
涉及表：oms_cart_item, oms_order, oms_order_item
"""

import pytest
from playwright.sync_api import Playwright
from config.settings import APP_API_BASE_URL
from api.app.services.cart_service import AppCartService
from api.app.services.order_service import AppOrderService
from utils.db.db_client import DBClient
from utils.data_loader import load_yaml


@pytest.fixture
def cart_service(playwright: Playwright, app_token: str):
    """已认证的 AppCartService 实例"""
    api_context = playwright.request.new_context(base_url=APP_API_BASE_URL)
    yield AppCartService(api_context, app_token)
    api_context.dispose()


@pytest.fixture
def order_service(playwright: Playwright, app_token: str):
    """已认证的 AppOrderService 实例"""
    api_context = playwright.request.new_context(base_url=APP_API_BASE_URL)
    yield AppOrderService(api_context, app_token)
    api_context.dispose()


@pytest.fixture
def test_data(request):
    """根据测试方法名自动加载对应测试数据"""
    data = load_yaml("api/test_app_order.yaml")
    return data[request.function.__name__]


class TestAppOrderFlow:
    """订单流程测试"""

    def test_add_cart_and_cancel_order(
        self,
        cart_service: AppCartService,
        order_service: AppOrderService,
        db: DBClient,
        test_data: dict,
    ):
        """加购 → 生成确认单 → 提交订单 → 取消订单"""
        # ==================== 1. 准备：查询商品和收货地址 ====================
        product_row = db.query(
            "SELECT id, price, name, brand_id, product_category_id "
            "FROM pms_product WHERE publish_status = 1 AND delete_status = 0 LIMIT 1"
        )
        assert len(product_row) > 0, "数据库中无上架商品"
        product_id = product_row[0]["id"]

        sku_row = db.query(
            "SELECT id FROM pms_sku_stock WHERE product_id = %s LIMIT 1",
            (product_id,),
        )
        assert len(sku_row) > 0, f"商品(ID={product_id})无 SKU 库存数据"
        product_sku_id = sku_row[0]["id"]

        address_row = db.query(
            "SELECT id FROM ums_member_receive_address "
            "WHERE member_id = 12 AND default_status = 1 LIMIT 1"
        )
        assert len(address_row) > 0, "数据库中无默认收货地址"
        address_id = address_row[0]["id"]

        # ==================== 2. 加购 ====================
        quantity = test_data["quantity"]
        resp = cart_service.add_cart(product_id, product_sku_id, quantity)
        assert resp.ok, f"加购请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"加购失败: {resp.json}"

        # 查询购物车中该商品的 cart_id
        cart_row = db.query(
            "SELECT id FROM oms_cart_item "
            "WHERE product_id = %s AND product_sku_id = %s AND delete_status = 0",
            (product_id, product_sku_id),
        )
        assert len(cart_row) > 0, "加购后数据库中未找到购物车记录"
        cart_ids = [cart_row[0]["id"]]

        # ==================== 3. 生成确认单 ====================
        resp = order_service.generate_confirm_order(cart_ids)
        assert resp.ok, f"生成确认单请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"生成确认单失败: {resp.json}"

        # ==================== 4. 提交订单 ====================
        order_param = {
            "memberReceiveAddressId": address_id,
            "useIntegration": test_data["use_integration"],
            "payType": test_data["pay_type"],
            "cartIds": cart_ids,
        }
        resp = order_service.generate_order(order_param)
        assert resp.ok, f"提交订单请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"提交订单失败: {resp.json}"
        order_id = resp.data["order"]["id"]
        assert order_id, f"提交订单未返回订单ID: {resp.json}"

        # 验证订单已创建
        order_row = db.query(
            "SELECT * FROM oms_order WHERE id = %s", (order_id,)
        )
        assert len(order_row) > 0, f"数据库中未找到订单: id={order_id}"
        order = order_row[0]
        assert order["status"] == 0, f"订单状态应为待付款(0)，实际: {order['status']}"
        assert order["delete_status"] in (0, None), \
            f"订单删除状态异常: {order['delete_status']}"

        # 验证订单明细
        item_rows = db.query(
            "SELECT * FROM oms_order_item WHERE order_id = %s", (order_id,)
        )
        assert len(item_rows) > 0, f"数据库中未找到订单明细: order_id={order_id}"
        assert item_rows[0]["product_id"] == product_id, \
            f"订单明细商品ID不匹配: 期望 {product_id}, 实际 {item_rows[0]['product_id']}"

        # ==================== 5. 取消订单 ====================
        resp = order_service.cancel_user_order(order_id)
        assert resp.ok, f"取消订单请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"取消订单失败: {resp.json}"

        # 验证订单已关闭
        order_after = db.query(
            "SELECT status FROM oms_order WHERE id = %s", (order_id,)
        )
        assert len(order_after) > 0, f"订单不存在: id={order_id}"
        assert order_after[0]["status"] == 4, \
            f"取消后订单状态应为已关闭(4)，实际: {order_after[0]['status']}"
