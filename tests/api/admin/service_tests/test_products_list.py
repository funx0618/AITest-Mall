"""
商品列表查询 API 测试用例
职责：验证后台管理商品查询接口
对应 API 文档：docs/api docs/admin-product-api.md
涉及表：pms_product
"""

import pytest
from playwright.sync_api import Playwright
from config.settings import ADMIN_API_BASE_URL
from api.admin.services.product_service import AdminProductService
from utils.db.db_client import DBClient
from utils.data_loader import load_yaml


@pytest.fixture
def product_service(playwright: Playwright, admin_token: str):
    """已认证的 AdminProductService 实例"""
    api_context = playwright.request.new_context(base_url=ADMIN_API_BASE_URL)
    yield AdminProductService(api_context, admin_token)
    api_context.dispose()


@pytest.fixture
def test_data(request):
    """根据测试方法名自动加载对应测试数据"""
    data = load_yaml("api/test_products_list.yaml")
    return data[request.function.__name__]


class TestProductsList:
    """商品列表查询接口测试"""

    def test_query_by_keyword(self, product_service: AdminProductService, db: DBClient, test_data: dict):
        """按商品名称关键字查询，与数据库对比"""
        keyword = test_data["keyword"]

        # 1. API 查询
        resp = product_service.get_product_list(keyword=keyword, page_num=1, page_size=100)
        assert resp.ok, f"API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"查询商品失败: {resp.json}"

        data = resp.data
        api_products = data.get("list", [])
        api_total = data.get("total", 0)

        # 2. 数据库查询
        sql = """
            SELECT COUNT(*) AS cnt FROM pms_product
            WHERE delete_status = 0
              AND name LIKE %s
        """
        keyword_pattern = f"%{keyword}%"
        db_total = db.query(sql, (keyword_pattern,))[0]["cnt"]

        # 3. 数量对比
        assert api_total == db_total, f"总数不一致: API={api_total}, DB={db_total}"

        # 4. 按 id 匹配对比关键字段
        if api_products:
            ids = [p["id"] for p in api_products]
            placeholders = ",".join(["%s"] * len(ids))
            sql_detail = f"""
                SELECT * FROM pms_product WHERE id IN ({placeholders})
            """
            db_products = db.query(sql_detail, tuple(ids))
            db_map = {row["id"]: row for row in db_products}

            for api_product in api_products:
                pid = api_product["id"]
                assert pid in db_map, f"API商品 ID={pid} 在数据库中不存在"
                db_product = db_map[pid]
                assert api_product["name"] == db_product["name"], f"商品名称不一致: ID={pid}"
                assert float(api_product["price"]) == float(db_product["price"]), f"商品价格不一致: ID={pid}"

    def test_query_by_publish_status(self, product_service: AdminProductService, db: DBClient, test_data: dict):
        """按上架状态查询商品，与数据库对比"""
        publish_status = test_data["publish_status"]

        # 1. API 查询
        resp = product_service.get_product_list(publish_status=publish_status, page_num=1, page_size=100)
        assert resp.ok, f"API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"查询商品失败: {resp.json}"

        data = resp.data
        api_total = data.get("total", 0)

        # 2. 数据库查询
        sql = """
            SELECT COUNT(*) AS cnt FROM pms_product
            WHERE delete_status = 0
              AND publish_status = %s
        """
        db_total = db.query(sql, (publish_status,))[0]["cnt"]

        # 3. 数量对比
        assert api_total == db_total, f"总数不一致: API={api_total}, DB={db_total}"

    def test_query_by_verify_status(self, product_service: AdminProductService, db: DBClient, test_data: dict):
        """按审核状态查询商品，与数据库对比"""
        verify_status = test_data["verify_status"]

        # 1. API 查询
        resp = product_service.get_product_list(verify_status=verify_status, page_num=1, page_size=100)
        assert resp.ok, f"API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"查询商品失败: {resp.json}"

        data = resp.data
        api_total = data.get("total", 0)

        # 2. 数据库查询
        sql = """
            SELECT COUNT(*) AS cnt FROM pms_product
            WHERE delete_status = 0
              AND verify_status = %s
        """
        db_total = db.query(sql, (verify_status,))[0]["cnt"]

        # 3. 数量对比
        assert api_total == db_total, f"总数不一致: API={api_total}, DB={db_total}"
