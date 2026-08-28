"""
订单流程测试 — 加购 → 确认单 → 提交订单 → 取消订单
职责：验证前台商城完整下单+取消流程
对应 API 文档：docs/api docs/app-api.md — OmsPortalOrderController
涉及表：oms_cart_item, oms_order, oms_order_item, sms_coupon, sms_coupon_history
"""

import pytest
from playwright.sync_api import Playwright
from config.settings import APP_API_BASE_URL
from api.app.cart_service import AppCartService
from api.app.coupon_service import AppCouponService
from api.app.order_service import AppOrderService
from utils.db.db_client import DBClient
from utils.data_loader import load_yaml


@pytest.fixture
def cart_service(playwright: Playwright, app_token: str):
    """已认证的 AppCartService 实例"""
    api_context = playwright.request.new_context(base_url=APP_API_BASE_URL)
    yield AppCartService(api_context, app_token)
    api_context.dispose()


@pytest.fixture
def coupon_service(playwright: Playwright, app_token: str):
    """已认证的 AppCouponService 实例"""
    api_context = playwright.request.new_context(base_url=APP_API_BASE_URL)
    yield AppCouponService(api_context, app_token)
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
    data = load_yaml("api/test_cancel_order_flow.yaml")
    return data[request.function.__name__]


class TestAppCancelOrderFlow:
    """订单流程测试"""

    def test_add_cart_and_cancel_order(
        self,
        cart_service: AppCartService,
        order_service: AppOrderService,
        db: DBClient,
        test_data: dict,
    ):
        """加购 → 生成确认单 → 提交订单 → 取消订单"""
        # ==================== 1. 准备：从YAML读取商品信息，查询收货地址 ====================
        product_id = test_data["product_id"]
        product_sku_id = test_data["sku_id"]

        # 验证商品存在且已上架
        product_row = db.query(
            "SELECT id, price, name FROM pms_product "
            "WHERE id = %s AND publish_status = 1 AND delete_status = 0",
            (product_id,),
        )
        assert len(product_row) > 0, f"未找到上架商品: id={product_id}"

        # 验证SKU存在
        sku_row = db.query(
            "SELECT id, price, stock FROM pms_sku_stock WHERE id = %s AND product_id = %s",
            (product_sku_id, product_id),
        )
        assert len(sku_row) > 0, f"商品(ID={product_id})无 SKU(ID={product_sku_id})库存数据"

        address_row = db.query(
            "SELECT id FROM ums_member_receive_address "
            "WHERE member_id = 12 AND default_status = 1 LIMIT 1"
        )
        assert len(address_row) > 0, "数据库中无默认收货地址"
        address_id = address_row[0]["id"]

        # ==================== 2. 加购 ====================
        quantity = test_data["quantity"]
        resp = cart_service.add_cart(product_id, product_sku_id, quantity)
        # 这里的resp的ok是判断接口通不通，code是判断业务成不成
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

        # 记录确认单中的期望金额
        calc_amount = resp.data["calcAmount"]
        expected_total = float(calc_amount["totalAmount"])
        expected_freight = float(calc_amount["freightAmount"])
        expected_promotion = float(calc_amount["promotionAmount"])
        expected_pay = float(calc_amount["payAmount"])

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

        # 验证订单金额（API 返回）
        order_data = resp.data["order"]
        assert float(order_data["totalAmount"]) == expected_total, \
            f"订单总金额不匹配: 期望 {expected_total}, 实际 {order_data['totalAmount']}"
        assert float(order_data["payAmount"]) == expected_pay, \
            f"订单实付金额不匹配: 期望 {expected_pay}, 实际 {order_data['payAmount']}"
        assert float(order_data["freightAmount"]) == expected_freight, \
            f"订单运费不匹配: 期望 {expected_freight}, 实际 {order_data['freightAmount']}"
        assert float(order_data["promotionAmount"]) == expected_promotion, \
            f"订单促销优惠不匹配: 期望 {expected_promotion}, 实际 {order_data['promotionAmount']}"

        # 验证订单已创建
        order_row = db.query(
            "SELECT * FROM oms_order WHERE id = %s", (order_id,)
        )
        assert len(order_row) > 0, f"数据库中未找到订单: id={order_id}"
        order = order_row[0]
        assert order["status"] == 0, f"订单状态应为待付款(0)，实际: {order['status']}"
        assert order["delete_status"] in (0, None), \
            f"订单删除状态异常: {order['delete_status']}"
        assert float(order["total_amount"]) == expected_total, \
            f"DB订单总金额不匹配: 期望 {expected_total}, 实际 {order['total_amount']}"
        assert float(order["pay_amount"]) == expected_pay, \
            f"DB订单实付金额不匹配: 期望 {expected_pay}, 实际 {order['pay_amount']}"

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

    def test_add_cart_with_coupon_and_cancel_order(
        self,
        cart_service: AppCartService,
        coupon_service: AppCouponService,
        order_service: AppOrderService,
        db: DBClient,
        test_data: dict,
    ):
        """加购 → 领取优惠券 → 生成确认单 → 使用优惠券提交订单 → 验证金额 → 取消订单"""
        # ==================== 1. 从DB获取基础数据，计算期望金额 ====================
        product_id = test_data["product_id"]
        product_sku_id = test_data["sku_id"]
        quantity = test_data["quantity"]

        # 验证商品存在且已上架
        product_row = db.query(
            "SELECT id, price, name, promotion_type FROM pms_product "
            "WHERE id = %s AND publish_status = 1 AND delete_status = 0",
            (product_id,),
        )
        assert len(product_row) > 0, f"未找到上架商品: id={product_id}"

        # 获取SKU价格和促销价
        sku_row = db.query(
            "SELECT id, price, promotion_price, stock FROM pms_sku_stock "
            "WHERE id = %s AND product_id = %s",
            (product_sku_id, product_id),
        )
        assert len(sku_row) > 0, f"商品(ID={product_id})无 SKU(ID={product_sku_id})库存数据"
        sku_price = float(sku_row[0]["price"])
        sku_promo_price = float(sku_row[0]["promotion_price"])

        # 获取优惠券金额
        coupon_name = test_data["coupon_name"]
        coupon_row = db.query(
            "SELECT id, amount, min_point FROM sms_coupon "
            "WHERE name = %s AND use_type = 0 AND start_time <= NOW() AND end_time >= NOW()",
            (coupon_name,),
        )
        assert len(coupon_row) > 0, f"未找到可用优惠券: {coupon_name}"
        coupon_id = coupon_row[0]["id"]
        expected_coupon = float(coupon_row[0]["amount"])

        # 查询收货地址
        address_row = db.query(
            "SELECT id FROM ums_member_receive_address "
            "WHERE member_id = 12 AND default_status = 1 LIMIT 1"
        )
        assert len(address_row) > 0, "数据库中无默认收货地址"
        address_id = address_row[0]["id"]

        # ==================== 2. 查询并领取优惠券 ====================
        # 检查会员是否已领取过该优惠券（任意状态）
        member_coupon_row = db.query(
            "SELECT id, coupon_id, use_status FROM sms_coupon_history "
            "WHERE coupon_id = %s AND member_id = 12",
            (coupon_id,),
        )

        if not member_coupon_row:
            # 未领取过，领取优惠券
            resp = coupon_service.add_coupon(coupon_id)
            assert resp.ok, f"领取优惠券请求失败: HTTP {resp.status_code}"
            assert resp.code == 200, f"领取优惠券失败: {resp.json}"

        # 取消订单后 use_status 仍然是 1，说明后端取消接口没有恢复优惠券。重置逻辑就是为了解决这个问题
        # 检查是否有未使用的优惠券，如果没有则重置最早的一条
        member_coupon_row = db.query(
            "SELECT id, coupon_id, use_status FROM sms_coupon_history "
            "WHERE coupon_id = %s AND member_id = 12 AND use_status = 0",
            (coupon_id,),
        )
        if not member_coupon_row:
            # 重置最早一条已使用记录，确保测试可重复执行
            
            db.query(
                "UPDATE sms_coupon_history SET use_status = 0, use_time = NULL "
                "WHERE coupon_id = %s AND member_id = 12 "
                "ORDER BY id ASC LIMIT 1",
                (coupon_id,),
            )
            member_coupon_row = db.query(
                "SELECT id, coupon_id, use_status FROM sms_coupon_history "
                "WHERE coupon_id = %s AND member_id = 12 AND use_status = 0",
                (coupon_id,),
            )
        assert len(member_coupon_row) > 0, f"会员无可用优惠券: coupon_id={coupon_id}"

        # ==================== 3. 清理购物车并加购 ====================
        # 清理该商品的已有购物车记录，避免数量累积
        db.query(
            "UPDATE oms_cart_item SET delete_status = 1 "
            "WHERE product_id = %s AND product_sku_id = %s AND delete_status = 0",
            (product_id, product_sku_id),
        )

        resp = cart_service.add_cart(product_id, product_sku_id, quantity)
        assert resp.ok, f"加购请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"加购失败: {resp.json}"

        # 查询购物车中该商品的 cart_id 和实际数量（可能已有历史残留）
        cart_row = db.query(
            "SELECT id, quantity FROM oms_cart_item "
            "WHERE product_id = %s AND product_sku_id = %s AND delete_status = 0",
            (product_id, product_sku_id),
        )
        assert len(cart_row) > 0, "加购后数据库中未找到购物车记录"
        cart_ids = [cart_row[0]["id"]]
        cart_quantity = int(cart_row[0]["quantity"])

        # ==================== 根据购物车实际数量计算期望金额 ====================
        # 商品合计 = 购物车数量 × SKU原价
        expected_total = cart_quantity * sku_price
        # 活动优惠 = (SKU原价 - SKU促销价) × 购物车数量
        expected_promotion = cart_quantity * (sku_price - sku_promo_price)
        # 积分抵扣 = 0（不使用积分）
        expected_integration = 0
        # 运费 = 0（订单金额大于免邮门槛）
        expected_freight = 0
        # 实付款 = 商品合计 + 运费 - 活动优惠 - 优惠券 - 积分抵扣
        expected_pay = max(
            expected_total + expected_freight - expected_promotion
            - expected_coupon - expected_integration,
            0,
        )

        # ==================== 4. 生成确认单 — 逐字段验证 ====================
        # 生成确认单时，还没有使用优惠卷，提交订单时才使用优惠卷
        resp = order_service.generate_confirm_order(cart_ids)
        assert resp.ok, f"生成确认单请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"生成确认单失败: {resp.json}"

        calc_amount = resp.data["calcAmount"]

        # 验证商品合计
        assert float(calc_amount["totalAmount"]) == expected_total, \
            f"确认单商品合计不匹配: 期望 {expected_total}, 实际 {calc_amount['totalAmount']}"
        # 验证运费
        assert float(calc_amount["freightAmount"]) == expected_freight, \
            f"确认单运费不匹配: 期望 {expected_freight}, 实际 {calc_amount['freightAmount']}"
        # 验证活动优惠
        assert float(calc_amount["promotionAmount"]) == expected_promotion, \
            f"确认单活动优惠不匹配: 期望 {expected_promotion}, 实际 {calc_amount['promotionAmount']}"

        # 确认单的实付款（未使用优惠券，实际付款 = 合计 + 运费 - 活动优惠）
        confirm_pay = float(calc_amount["payAmount"])
        expected_confirm_pay = max(expected_total + expected_freight - expected_promotion, 0)
        assert confirm_pay == expected_confirm_pay, \
            f"确认单实付款不匹配: 期望 {expected_confirm_pay}, 实际 {confirm_pay}"

        # 验证确认单中包含该优惠券
        coupon_list = resp.data.get("couponHistoryDetailList", [])
        coupon_found = any(c.get("couponId") == coupon_id for c in coupon_list)
        assert coupon_found, f"确认单中未包含优惠券: {coupon_name}"

        # ==================== 5. 使用优惠券提交订单 — 仅验证实付款 ====================
        order_param = {
            "memberReceiveAddressId": address_id,
            "couponId": coupon_id,
            "useIntegration": test_data["use_integration"],
            "payType": test_data["pay_type"],
            "cartIds": cart_ids,
        }
        resp = order_service.generate_order(order_param)
        assert resp.ok, f"提交订单请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"提交订单失败: {resp.json}"
        order_id = resp.data["order"]["id"]
        assert order_id, f"提交订单未返回订单ID: {resp.json}"

        # 验证实付款（与确认单一致）
        order_data = resp.data["order"]
        assert float(order_data["payAmount"]) == expected_pay, \
            f"订单实付款不匹配: 期望 {expected_pay}, 实际 {order_data['payAmount']}"

        # ==================== 6. 验证数据库订单记录 ====================
        order_row = db.query(
            "SELECT * FROM oms_order WHERE id = %s", (order_id,)
        )
        assert len(order_row) > 0, f"数据库中未找到订单: id={order_id}"
        order = order_row[0]
        assert order["status"] == 0, f"订单状态应为待付款(0)，实际: {order['status']}"
        assert order["delete_status"] in (0, None), \
            f"订单删除状态异常: {order['delete_status']}"
        assert float(order["total_amount"]) == expected_total, \
            f"DB订单商品合计不匹配: 期望 {expected_total}, 实际 {order['total_amount']}"
        assert float(order["pay_amount"]) == expected_pay, \
            f"DB订单实付款不匹配: 期望 {expected_pay}, 实际 {order['pay_amount']}"
        assert float(order["freight_amount"]) == expected_freight, \
            f"DB订单运费不匹配: 期望 {expected_freight}, 实际 {order['freight_amount']}"
        assert float(order["promotion_amount"]) == expected_promotion, \
            f"DB订单活动优惠不匹配: 期望 {expected_promotion}, 实际 {order['promotion_amount']}"
        assert order["coupon_id"] == coupon_id, \
            f"DB订单优惠券ID不匹配: 期望 {coupon_id}, 实际 {order['coupon_id']}"
        assert float(order["coupon_amount"]) == expected_coupon, \
            f"DB订单优惠券抵扣不匹配: 期望 {expected_coupon}, 实际 {order['coupon_amount']}"

        # 验证优惠券使用状态已更新
        coupon_history_after = db.query(
            "SELECT use_status, use_time FROM sms_coupon_history "
            "WHERE coupon_id = %s AND member_id = 12 ORDER BY id DESC LIMIT 1",
            (coupon_id,),
        )
        assert len(coupon_history_after) > 0, "未找到优惠券使用记录"
        assert coupon_history_after[0]["use_status"] == 1, \
            f"优惠券使用状态应为已使用(1)，实际: {coupon_history_after[0]['use_status']}"

        # 验证订单明细
        item_rows = db.query(
            "SELECT * FROM oms_order_item WHERE order_id = %s", (order_id,)
        )
        assert len(item_rows) > 0, f"数据库中未找到订单明细: order_id={order_id}"
        assert item_rows[0]["product_id"] == product_id, \
            f"订单明细商品ID不匹配: 期望 {product_id}, 实际 {item_rows[0]['product_id']}"
        assert float(item_rows[0]["coupon_amount"]) == expected_coupon, \
            f"订单明细优惠券抵扣不匹配: 期望 {expected_coupon}, 实际 {item_rows[0]['coupon_amount']}"

        # ==================== 7. 取消订单 ====================
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

    def test_add_cart_with_flash_coupon_and_cancel_order(
        self,
        cart_service: AppCartService,
        coupon_service: AppCouponService,
        order_service: AppOrderService,
        db: DBClient,
        test_data: dict,
    ):
        """加购(秒杀商品) → 领取优惠券 → 生成确认单 → 使用优惠券提交订单 → 验证价格(秒杀+优惠券) → 取消订单"""
        # ==================== 1. 从DB获取秒杀活动信息，计算期望金额 ====================
        product_id = test_data["product_id"]
        product_sku_id = test_data["sku_id"]
        quantity = test_data["quantity"]

        # 验证商品存在且已上架
        product_row = db.query(
            "SELECT id, price, name, promotion_type FROM pms_product "
            "WHERE id = %s AND publish_status = 1 AND delete_status = 0",
            (product_id,),
        )
        assert len(product_row) > 0, f"未找到上架商品: id={product_id}"

        # 获取SKU价格
        sku_row = db.query(
            "SELECT id, price, promotion_price, stock FROM pms_sku_stock "
            "WHERE id = %s AND product_id = %s",
            (product_sku_id, product_id),
        )
        assert len(sku_row) > 0, f"商品(ID={product_id})无 SKU(ID={product_sku_id})库存数据"
        sku_price = float(sku_row[0]["price"])

        # 获取当前有效的秒杀活动与场次
        flash_relation = db.query(
            "SELECT r.flash_promotion_id, r.flash_promotion_session_id, "
            "r.flash_promotion_price, r.flash_promotion_count, r.flash_promotion_limit "
            "FROM sms_flash_promotion_product_relation r "
            "JOIN sms_flash_promotion p ON r.flash_promotion_id = p.id "
            "JOIN sms_flash_promotion_session s ON r.flash_promotion_session_id = s.id "
            "WHERE r.product_id = %s "
            "AND p.status = 1 AND p.start_date <= CURDATE() AND p.end_date >= CURDATE() "
            "AND s.status = 1 AND s.start_time <= CURTIME() AND s.end_time >= CURTIME() "
            "AND r.flash_promotion_price IS NOT NULL",
            (product_id,),
        )
        assert len(flash_relation) > 0, \
            f"商品(ID={product_id})当前无有效秒杀活动"
        flash_promo = flash_relation[0]
        flash_promotion_id = flash_promo["flash_promotion_id"]
        flash_session_id = flash_promo["flash_promotion_session_id"]
        flash_price = float(flash_promo["flash_promotion_price"])
        flash_limit = int(flash_promo["flash_promotion_limit"])
        assert quantity <= flash_limit, \
            f"购买数量({quantity})超过秒杀限购数({flash_limit})"

        # 获取优惠券金额
        coupon_name = test_data["coupon_name"]
        coupon_row = db.query(
            "SELECT id, amount, min_point FROM sms_coupon "
            "WHERE name = %s AND use_type = 0 AND start_time <= NOW() AND end_time >= NOW()",
            (coupon_name,),
        )
        assert len(coupon_row) > 0, f"未找到可用优惠券: {coupon_name}"
        coupon_id = coupon_row[0]["id"]
        expected_coupon = float(coupon_row[0]["amount"])

        # 查询收货地址
        address_row = db.query(
            "SELECT id FROM ums_member_receive_address "
            "WHERE member_id = 12 AND default_status = 1 LIMIT 1"
        )
        assert len(address_row) > 0, "数据库中无默认收货地址"
        address_id = address_row[0]["id"]

        # ==================== 2. 查询并领取优惠券 ====================
        member_coupon_row = db.query(
            "SELECT id, coupon_id, use_status FROM sms_coupon_history "
            "WHERE coupon_id = %s AND member_id = 12",
            (coupon_id,),
        )

        if not member_coupon_row:
            resp = coupon_service.add_coupon(coupon_id)
            assert resp.ok, f"领取优惠券请求失败: HTTP {resp.status_code}"
            assert resp.code == 200, f"领取优惠券失败: {resp.json}"

        # 检查是否有未使用的优惠券，如果没有则重置最早的一条
        member_coupon_row = db.query(
            "SELECT id, coupon_id, use_status FROM sms_coupon_history "
            "WHERE coupon_id = %s AND member_id = 12 AND use_status = 0",
            (coupon_id,),
        )
        if not member_coupon_row:
            db.query(
                "UPDATE sms_coupon_history SET use_status = 0, use_time = NULL "
                "WHERE coupon_id = %s AND member_id = 12 "
                "ORDER BY id ASC LIMIT 1",
                (coupon_id,),
            )
            member_coupon_row = db.query(
                "SELECT id, coupon_id, use_status FROM sms_coupon_history "
                "WHERE coupon_id = %s AND member_id = 12 AND use_status = 0",
                (coupon_id,),
            )
        assert len(member_coupon_row) > 0, f"会员无可用优惠券: coupon_id={coupon_id}"

        # ==================== 3. 清理购物车并加购 ====================
        db.query(
            "UPDATE oms_cart_item SET delete_status = 1 "
            "WHERE product_id = %s AND product_sku_id = %s AND delete_status = 0",
            (product_id, product_sku_id),
        )

        resp = cart_service.add_cart(product_id, product_sku_id, quantity)
        assert resp.ok, f"加购请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"加购失败: {resp.json}"

        # 查询购物车中该商品的 cart_id 和实际数量
        cart_row = db.query(
            "SELECT id, quantity FROM oms_cart_item "
            "WHERE product_id = %s AND product_sku_id = %s AND delete_status = 0",
            (product_id, product_sku_id),
        )
        assert len(cart_row) > 0, "加购后数据库中未找到购物车记录"
        cart_ids = [cart_row[0]["id"]]
        cart_quantity = int(cart_row[0]["quantity"])

        # ==================== 根据秒杀价格计算期望金额 ====================
        # 商品合计 = 购物车数量 × SKU原价
        expected_total = cart_quantity * sku_price
        # 秒杀优惠 = (SKU原价 - 秒杀价) × 购物车数量
        expected_promotion = cart_quantity * (sku_price - flash_price)
        # 积分抵扣 = 0（不使用积分）
        expected_integration = 0
        # 运费 = 0（订单金额大于免邮门槛）
        expected_freight = 0
        # 实付款 = 商品合计 + 运费 - 秒杀优惠 - 优惠券 - 积分抵扣
        expected_pay = max(
            expected_total + expected_freight - expected_promotion
            - expected_coupon - expected_integration,
            0,
        )

        # ==================== 4. 生成确认单 — 逐字段验证 ====================
        resp = order_service.generate_confirm_order(cart_ids)
        assert resp.ok, f"生成确认单请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"生成确认单失败: {resp.json}"

        calc_amount = resp.data["calcAmount"]

        # 验证商品合计
        assert float(calc_amount["totalAmount"]) == expected_total, \
            f"确认单商品合计不匹配: 期望 {expected_total}, 实际 {calc_amount['totalAmount']}"
        # 验证运费
        assert float(calc_amount["freightAmount"]) == expected_freight, \
            f"确认单运费不匹配: 期望 {expected_freight}, 实际 {calc_amount['freightAmount']}"
        # 验证秒杀优惠（promotionAmount）
        assert float(calc_amount["promotionAmount"]) == expected_promotion, \
            f"确认单秒杀优惠不匹配: 期望 {expected_promotion}, 实际 {calc_amount['promotionAmount']}"

        # 确认单的实付款（未使用优惠券，实际付款 = 合计 + 运费 - 秒杀优惠）
        confirm_pay = float(calc_amount["payAmount"])
        expected_confirm_pay = max(expected_total + expected_freight - expected_promotion, 0)
        assert confirm_pay == expected_confirm_pay, \
            f"确认单实付款不匹配: 期望 {expected_confirm_pay}, 实际 {confirm_pay}"

        # 验证确认单中包含该优惠券
        coupon_list = resp.data.get("couponHistoryDetailList", [])
        coupon_found = any(c.get("couponId") == coupon_id for c in coupon_list)
        assert coupon_found, f"确认单中未包含优惠券: {coupon_name}"

        # ==================== 5. 使用优惠券提交订单 ====================
        order_param = {
            "memberReceiveAddressId": address_id,
            "couponId": coupon_id,
            "useIntegration": test_data["use_integration"],
            "payType": test_data["pay_type"],
            "cartIds": cart_ids,
        }
        resp = order_service.generate_order(order_param)
        assert resp.ok, f"提交订单请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"提交订单失败: {resp.json}"
        order_id = resp.data["order"]["id"]
        assert order_id, f"提交订单未返回订单ID: {resp.json}"

        # 验证实付款（与确认单一致，扣除优惠券）
        order_data = resp.data["order"]
        assert float(order_data["payAmount"]) == expected_pay, \
            f"订单实付款不匹配: 期望 {expected_pay}, 实际 {order_data['payAmount']}"

        # ==================== 6. 验证数据库订单记录 ====================
        order_row = db.query(
            "SELECT * FROM oms_order WHERE id = %s", (order_id,)
        )
        assert len(order_row) > 0, f"数据库中未找到订单: id={order_id}"
        order = order_row[0]
        assert order["status"] == 0, f"订单状态应为待付款(0)，实际: {order['status']}"
        assert order["delete_status"] in (0, None), \
            f"订单删除状态异常: {order['delete_status']}"
        assert float(order["total_amount"]) == expected_total, \
            f"DB订单商品合计不匹配: 期望 {expected_total}, 实际 {order['total_amount']}"
        assert float(order["pay_amount"]) == expected_pay, \
            f"DB订单实付款不匹配: 期望 {expected_pay}, 实际 {order['pay_amount']}"
        assert float(order["freight_amount"]) == expected_freight, \
            f"DB订单运费不匹配: 期望 {expected_freight}, 实际 {order['freight_amount']}"
        assert float(order["promotion_amount"]) == expected_promotion, \
            f"DB订单秒杀优惠不匹配: 期望 {expected_promotion}, 实际 {order['promotion_amount']}"
        assert order["coupon_id"] == coupon_id, \
            f"DB订单优惠券ID不匹配: 期望 {coupon_id}, 实际 {order['coupon_id']}"
        assert float(order["coupon_amount"]) == expected_coupon, \
            f"DB订单优惠券抵扣不匹配: 期望 {expected_coupon}, 实际 {order['coupon_amount']}"

        # 验证优惠券使用状态已更新
        coupon_history_after = db.query(
            "SELECT use_status, use_time FROM sms_coupon_history "
            "WHERE coupon_id = %s AND member_id = 12 ORDER BY id DESC LIMIT 1",
            (coupon_id,),
        )
        assert len(coupon_history_after) > 0, "未找到优惠券使用记录"
        assert coupon_history_after[0]["use_status"] == 1, \
            f"优惠券使用状态应为已使用(1)，实际: {coupon_history_after[0]['use_status']}"

        # 验证订单明细
        item_rows = db.query(
            "SELECT * FROM oms_order_item WHERE order_id = %s", (order_id,)
        )
        assert len(item_rows) > 0, f"数据库中未找到订单明细: order_id={order_id}"
        assert item_rows[0]["product_id"] == product_id, \
            f"订单明细商品ID不匹配: 期望 {product_id}, 实际 {item_rows[0]['product_id']}"
        assert float(item_rows[0]["coupon_amount"]) == expected_coupon, \
            f"订单明细优惠券抵扣不匹配: 期望 {expected_coupon}, 实际 {item_rows[0]['coupon_amount']}"

        # ==================== 7. 取消订单 ====================
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
