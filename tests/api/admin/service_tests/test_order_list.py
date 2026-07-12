"""
Order API 测试用例
职责：验证后台管理订单查询接口
"""

import pytest
from playwright.sync_api import Playwright
from config.settings import ADMIN_API_BASE_URL
from api.admin.services.order_service import AdminOrderService
from utils.db.db_client import DBClient
from utils.data_loader import load_yaml


@pytest.fixture
def order_service(playwright: Playwright, admin_token: str):
    """已认证的 AdminOrderService 实例"""
    api_context = playwright.request.new_context(base_url=ADMIN_API_BASE_URL)
    yield AdminOrderService(api_context, admin_token)
    api_context.dispose()


@pytest.fixture
def db():
    """数据库客户端实例"""
    client = DBClient()
    yield client
    client.close()


@pytest.fixture
def test_data(request):
    """根据测试方法名自动加载对应测试数据"""
    data = load_yaml("api/test_order_list.yaml")
    return data[request.function.__name__]


class TestOrderList:
    """订单列表接口测试"""

    def test_query_by_receiver_status(self, order_service: AdminOrderService, db: DBClient, test_data: dict):
        """按收货人和订单状态查询，与数据库对比"""
        # 测试数据
        receiver_keyword = test_data["receiver_keyword"]
        status = test_data["status"]

        # 1. API 查询
        resp = order_service.get_order_list(
            page_num=1,
            page_size=10,
            status=status,
            receiverKeyword=receiver_keyword,
        )
        assert resp.ok, f"API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"查询订单失败: {resp.json}"

        data = resp.data
        api_orders = data.get("list", [])
        api_total = data.get("total", 0)
        assert api_total > 0, f"未查询到 {receiver_keyword} 的已发货订单"

        # 2. 数据库查询
        sql = """
            SELECT * FROM oms_order
            WHERE delete_status = 0
              AND status = %s
              AND (receiver_name LIKE %s OR receiver_phone LIKE %s)
            ORDER BY create_time DESC
            LIMIT %s
        """
        keyword_pattern = f"%{receiver_keyword}%"
        db_orders = db.query(sql, (status, keyword_pattern, keyword_pattern, 10))

        # 3. 数量对比
        db_total_sql = """
            SELECT COUNT(*) AS cnt FROM oms_order
            WHERE delete_status = 0
              AND status = %s
              AND (receiver_name LIKE %s OR receiver_phone LIKE %s)
        """
        db_total = db.query(db_total_sql, (status, keyword_pattern, keyword_pattern))[0]["cnt"]
        assert api_total == db_total, f"总数不一致: API={api_total}, DB={db_total}"

        # 4. 按 orderSn 匹配对比关键字段
        db_map = {row["order_sn"]: row for row in db_orders}
        for api_order in api_orders:
            sn = api_order["orderSn"]
            assert sn in db_map, f"API订单 {sn} 在数据库中不存在"
            db_order = db_map[sn]
            assert api_order["memberUsername"] == db_order["member_username"], f"用户账号不一致: {sn}"
            assert api_order["totalAmount"] == float(db_order["total_amount"]), f"订单金额不一致: {sn}"
            assert api_order["payType"] == db_order["pay_type"], f"支付方式不一致: {sn}"
            assert api_order["status"] == db_order["status"], f"订单状态不一致: {sn}"

    def test_query_by_create_time(self, order_service: AdminOrderService, db: DBClient, test_data: dict):
        """按提交时间查询订单，对比数量"""
        create_time = test_data["create_time"]

        # 1. API 查询
        resp = order_service.get_order_list(
            page_num=1,
            page_size=100,
            createTime=create_time,
        )
        assert resp.ok, f"API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"查询订单失败: {resp.json}"

        api_total = resp.data.get("total", 0)

        # 2. 数据库查询
        sql = """
            SELECT COUNT(*) AS cnt FROM oms_order
            WHERE delete_status = 0
              AND DATE(create_time) = %s
        """
        db_total = db.query(sql, (create_time,))[0]["cnt"]

        # 3. 数量对比
        assert api_total == db_total, f"总数不一致: API={api_total}, DB={db_total}"
