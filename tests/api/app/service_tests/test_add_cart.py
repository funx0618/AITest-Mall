"""
添加购物车 API 测试用例
职责：验证前台商城添加购物车接口
对应 API 文档：docs/api docs/app-api.md — OmsCartItemController
涉及表：oms_cart_item, pms_product, pms_sku_stock
"""

import pytest
from playwright.sync_api import Playwright
from config.settings import APP_API_BASE_URL
from api.app.services.cart_service import AppCartService
from utils.db.db_client import DBClient
from utils.data_loader import load_yaml


@pytest.fixture
def cart_service(playwright: Playwright, app_token: str):
    """已认证的 AppCartService 实例"""
    api_context = playwright.request.new_context(base_url=APP_API_BASE_URL)
    yield AppCartService(api_context, app_token)
    api_context.dispose()


@pytest.fixture
def test_data(request):
    """根据测试方法名自动加载对应测试数据"""
    data = load_yaml("api/test_add_cart.yaml")
    return data[request.function.__name__]


class TestAddCart:
    """添加购物车接口测试"""

    def test_add_cart(self, cart_service: AppCartService, db: DBClient, test_data: dict):
        """添加商品到购物车后验证 oms_cart_item 表数据落库正确"""
        # 0. 查询数据库中已上架且有 SKU 库存的商品（确保商品有效）
        product_row = db.query(
            "SELECT id FROM pms_product WHERE publish_status = 1 AND delete_status = 0 LIMIT 1"
        )
        assert len(product_row) > 0, "数据库中无上架商品，无法添加购物车"
        product_id = product_row[0]["id"]

        sku_row = db.query(
            "SELECT id FROM pms_sku_stock WHERE product_id = %s LIMIT 1",
            (product_id,),
        )
        assert len(sku_row) > 0, f"商品(ID={product_id})无 SKU 库存数据"
        product_sku_id = sku_row[0]["id"]

        # 1. 记录添加前购物车中该商品的数量（可能已存在）
        before_row = db.query(
            "SELECT quantity FROM oms_cart_item WHERE product_id = %s AND product_sku_id = %s AND delete_status = 0",
            (product_id, product_sku_id),
        )
        before_quantity = before_row[0]["quantity"] if before_row else 0

        # 2. API 添加商品到购物车
        quantity = test_data["quantity"]
        resp = cart_service.add_cart(product_id, product_sku_id, quantity)
        assert resp.ok, f"API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"添加购物车失败: {resp.json}"

        # 3. 数据库验证 - oms_cart_item 表
        db_result = db.query(
            "SELECT * FROM oms_cart_item WHERE product_id = %s AND product_sku_id = %s AND delete_status = 0",
            (product_id, product_sku_id),
        )
        assert len(db_result) > 0, f"数据库中未找到购物车记录: productId={product_id}, skuId={product_sku_id}"
        cart_item = db_result[0]
        cart_item_id = cart_item["id"]

        expected_quantity = before_quantity + quantity
        assert cart_item["quantity"] == expected_quantity, \
            f"购物车数量不匹配: 期望 {expected_quantity}, 实际 {cart_item['quantity']}"
        assert cart_item["product_id"] == product_id, \
            f"商品ID不匹配: 期望 {product_id}, 实际 {cart_item['product_id']}"
        assert cart_item["product_sku_id"] == product_sku_id, \
            f"SKU ID不匹配: 期望 {product_sku_id}, 实际 {cart_item['product_sku_id']}"
        assert cart_item["delete_status"] == 0, \
            f"删除状态异常: 期望 0, 实际 {cart_item['delete_status']}"

        # 4. 清理：删除测试添加的购物车记录
        clean_resp = cart_service.delete_cart([cart_item_id])
        assert clean_resp.ok, f"清理购物车API请求失败: HTTP {clean_resp.status_code}"
        assert clean_resp.code == 200, f"清理购物车失败: {clean_resp.json}"

        # 5. 数据库验证购物车记录已删除
        db_after = db.query(
            "SELECT delete_status FROM oms_cart_item WHERE id = %s",
            (cart_item_id,),
        )
        assert len(db_after) > 0, f"购物车记录不存在: id={cart_item_id}"
        assert db_after[0]["delete_status"] == 1, \
            f"购物车记录未被软删除: id={cart_item_id}, delete_status={db_after[0]['delete_status']}"
