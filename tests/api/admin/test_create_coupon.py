"""
创建优惠券 API 测试用例
职责：验证后台管理创建优惠券接口
对应 API 文档：docs/api docs/admin-coupon-api.md
涉及表：sms_coupon, sms_coupon_product_relation, sms_coupon_product_category_relation
"""

import pytest
from datetime import datetime, timedelta
from playwright.sync_api import Playwright
from config.settings import ADMIN_API_BASE_URL
from api.admin.coupon_service import AdminCouponService
from utils.db.db_client import DBClient
from utils.data_loader import load_yaml


@pytest.fixture
def coupon_service(playwright: Playwright, admin_token: str):
    """已认证的 AdminCouponService 实例"""
    api_context = playwright.request.new_context(base_url=ADMIN_API_BASE_URL)
    yield AdminCouponService(api_context, admin_token)
    api_context.dispose()


@pytest.fixture
def test_data(request):
    """根据测试方法名自动加载对应测试数据"""
    data = load_yaml("api/test_create_coupon.yaml")
    return data[request.function.__name__]


class TestCreateCoupon:
    """创建优惠券接口测试"""

    def test_create_coupon(self, coupon_service: AdminCouponService, db: DBClient, test_data: dict):
        """创建优惠券后验证 sms_coupon 表数据落库正确，最后清理数据"""
        # ==================== 1. 构造请求参数 ====================
        now = datetime.now()
        coupon_param = {
            "type": test_data["type"],
            "name": test_data["name"],
            "platform": test_data["platform"],
            "amount": test_data["amount"],
            "perLimit": test_data["per_limit"],
            "useType": test_data["use_type"],
            "productRelationList": [],
            "productCategoryRelationList": [],
            "publishCount": test_data["publish_count"],
            "minPoint": test_data["min_point"],
            "enableTime": (now + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "startTime": (now + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "endTime": (now + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "note": test_data["note"],
            "code": test_data["code"],
            "memberLevel": test_data["member_level"],
        }

        # ==================== 2. 创建优惠券 ====================
        resp = coupon_service.create_coupon(coupon_param)
        assert resp.ok, f"创建优惠券请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"创建优惠券失败: {resp.json}"

        # ==================== 3. 数据库验证 ====================
        sql = """
            SELECT * FROM sms_coupon
            WHERE code = %s
            ORDER BY id DESC
            LIMIT 1
        """
        db_result = db.query(sql, (test_data["code"],))
        assert len(db_result) > 0, f"数据库中未找到优惠券: code={test_data['code']}"
        coupon = db_result[0]
        coupon_id = coupon["id"]

        assert coupon["name"] == test_data["name"], \
            f"优惠券名称不匹配: 期望 {test_data['name']}, 实际 {coupon['name']}"
        assert coupon["type"] == test_data["type"], \
            f"优惠券类型不匹配: 期望 {test_data['type']}, 实际 {coupon['type']}"
        assert coupon["platform"] == test_data["platform"], \
            f"使用平台不匹配: 期望 {test_data['platform']}, 实际 {coupon['platform']}"
        assert float(coupon["amount"]) == test_data["amount"], \
            f"金额不匹配: 期望 {test_data['amount']}, 实际 {coupon['amount']}"
        assert coupon["per_limit"] == test_data["per_limit"], \
            f"每人限领不匹配: 期望 {test_data['per_limit']}, 实际 {coupon['per_limit']}"
        assert float(coupon["min_point"]) == test_data["min_point"], \
            f"使用门槛不匹配: 期望 {test_data['min_point']}, 实际 {coupon['min_point']}"
        assert coupon["use_type"] == test_data["use_type"], \
            f"使用类型不匹配: 期望 {test_data['use_type']}, 实际 {coupon['use_type']}"
        assert coupon["publish_count"] == test_data["publish_count"], \
            f"发行数量不匹配: 期望 {test_data['publish_count']}, 实际 {coupon['publish_count']}"
        assert coupon["member_level"] == test_data["member_level"], \
            f"会员等级不匹配: 期望 {test_data['member_level']}, 实际 {coupon['member_level']}"

        # ==================== 4. 清理：删除优惠券 ====================
        resp = coupon_service.delete_coupon(coupon_id)
        assert resp.ok, f"删除优惠券请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"删除优惠券失败: {resp.json}"

        # 验证已删除
        db_after = db.query("SELECT * FROM sms_coupon WHERE id = %s", (coupon_id,))
        assert len(db_after) == 0, f"优惠券未被删除: id={coupon_id}"
