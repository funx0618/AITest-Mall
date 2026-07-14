"""
商品分类业务流程测试用例
职责：验证后台管理商品分类的完整业务流程
对应 API 文档：docs/api docs/admin-product-api.md
涉及表：pms_product_category, pms_product_category_attribute_relation

业务流程：
1. 创建分类（显示状态） -> 修改显示状态为隐藏 -> 删除分类
2. 创建分类（隐藏状态） -> 修改导航栏状态为显示 -> 删除分类
"""

import pytest
from playwright.sync_api import Playwright
from config.settings import ADMIN_API_BASE_URL
from api.admin.services.product_category_service import AdminProductCategoryService
from utils.db.db_client import DBClient
from utils.data_loader import load_yaml


@pytest.fixture
def category_service(playwright: Playwright, admin_token: str):
    """已认证的 AdminProductCategoryService 实例"""
    api_context = playwright.request.new_context(base_url=ADMIN_API_BASE_URL)
    yield AdminProductCategoryService(api_context, admin_token)
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
    data = load_yaml("api/test_product_category_flow.yaml")
    return data[request.function.__name__]


class TestProductCategoryFlow:
    """商品分类业务流程测试"""

    def test_create_category_visible(self, category_service: AdminProductCategoryService, db: DBClient, test_data: dict):
        """创建显示分类 -> 修改显示状态为隐藏 -> 删除分类"""
        # 测试数据
        category_param = {
            "parentId": test_data["parent_id"],
            "name": test_data["name"],
            "productUnit": test_data["product_unit"],
            "navStatus": test_data["nav_status"],
            "showStatus": test_data["show_status"],
            "sort": test_data["sort"],
            "icon": test_data["icon"],
            "keywords": test_data["keywords"],
            "description": test_data["description"],
            "productAttributeIdList": test_data["product_attribute_id_list"],
        }

        # 1. API 创建分类
        resp = category_service.create_category(category_param)
        assert resp.ok, f"API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"创建分类失败: {resp.json}"

        # 2. 数据库验证 - pms_product_category 表
        sql = """
            SELECT * FROM pms_product_category
            WHERE name = %s AND parent_id = %s
            ORDER BY id DESC
            LIMIT 1
        """
        db_result = db.query(sql, (test_data["name"], test_data["parent_id"]))
        assert len(db_result) > 0, f"数据库中未找到分类: {test_data['name']}"
        category = db_result[0]
        category_id = category["id"]
        assert category["show_status"] == test_data["show_status"], \
            f"show_status 不匹配: 期望 {test_data['show_status']}, 实际 {category['show_status']}"
        assert category["nav_status"] == test_data["nav_status"], \
            f"nav_status 不匹配: 期望 {test_data['nav_status']}, 实际 {category['nav_status']}"
        assert category["product_unit"] == test_data["product_unit"], \
            f"product_unit 不匹配: 期望 {test_data['product_unit']}, 实际 {category['product_unit']}"
        assert category["keywords"] == test_data["keywords"], \
            f"keywords 不匹配: 期望 {test_data['keywords']}, 实际 {category['keywords']}"
        assert category["description"] == test_data["description"], \
            f"description 不匹配: 期望 {test_data['description']}, 实际 {category['description']}"

        # 3. 调用 detail API 验证分类已创建
        detail_resp = category_service.get_category_detail(category_id)
        assert detail_resp.ok, f"获取分类详情API请求失败: HTTP {detail_resp.status_code}"
        assert detail_resp.json["data"]["name"] == test_data["name"], \
            f"分类名称不匹配: 期望 {test_data['name']}, 实际 {detail_resp.json['data']['name']}"

        # 4. 调用 API 将显示状态改为隐藏（showStatus: 1 -> 0）
        resp = category_service.update_show_status([category_id], 0)
        assert resp.ok, f"修改显示状态API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"修改显示状态失败: {resp.json}"

        # 5. 数据库验证 - show_status 已更新为 0
        sql_verify = """
            SELECT show_status FROM pms_product_category WHERE id = %s
        """
        db_result = db.query(sql_verify, (category_id,))
        assert db_result[0]["show_status"] == 0, \
            f"show_status 更新失败: 期望 0, 实际 {db_result[0]['show_status']}"

        # 6. 调用 API 删除分类
        resp = category_service.delete_category(category_id)
        assert resp.ok, f"删除分类API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"删除分类失败: {resp.json}"

        # 7. 数据库验证 - 分类已被删除
        sql_delete = """
            SELECT COUNT(*) AS cnt FROM pms_product_category WHERE id = %s
        """
        db_result = db.query(sql_delete, (category_id,))
        assert db_result[0]["cnt"] == 0, f"分类未被删除: ID={category_id}"

    def test_create_category_hidden(self, category_service: AdminProductCategoryService, db: DBClient, test_data: dict):
        """创建隐藏分类 -> 修改导航栏状态为显示 -> 删除分类"""
        # 测试数据
        category_param = {
            "parentId": test_data["parent_id"],
            "name": test_data["name"],
            "productUnit": test_data["product_unit"],
            "navStatus": test_data["nav_status"],
            "showStatus": test_data["show_status"],
            "sort": test_data["sort"],
            "icon": test_data["icon"],
            "keywords": test_data["keywords"],
            "description": test_data["description"],
            "productAttributeIdList": test_data["product_attribute_id_list"],
        }

        # 1. API 创建分类
        resp = category_service.create_category(category_param)
        assert resp.ok, f"API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"创建分类失败: {resp.json}"

        # 2. 数据库验证 - pms_product_category 表
        sql = """
            SELECT * FROM pms_product_category
            WHERE name = %s AND parent_id = %s
            ORDER BY id DESC
            LIMIT 1
        """
        db_result = db.query(sql, (test_data["name"], test_data["parent_id"]))
        assert len(db_result) > 0, f"数据库中未找到分类: {test_data['name']}"

        category = db_result[0]
        category_id = category["id"]
        assert category["show_status"] == test_data["show_status"], \
            f"show_status 不匹配: 期望 {test_data['show_status']}, 实际 {category['show_status']}"
        assert category["nav_status"] == test_data["nav_status"], \
            f"nav_status 不匹配: 期望 {test_data['nav_status']}, 实际 {category['nav_status']}"
        assert category["product_unit"] == test_data["product_unit"], \
            f"product_unit 不匹配: 期望 {test_data['product_unit']}, 实际 {category['product_unit']}"
        assert category["keywords"] == test_data["keywords"], \
            f"keywords 不匹配: 期望 {test_data['keywords']}, 实际 {category['keywords']}"
        assert category["description"] == test_data["description"], \
            f"description 不匹配: 期望 {test_data['description']}, 实际 {category['description']}"

        # 3. 调用 detail API 验证分类已创建
        detail_resp = category_service.get_category_detail(category_id)
        assert detail_resp.ok, f"获取分类详情API请求失败: HTTP {detail_resp.status_code}"
        assert detail_resp.json["data"]["name"] == test_data["name"], \
            f"分类名称不匹配: 期望 {test_data['name']}, 实际 {detail_resp.json['data']['name']}"

        # 4. 调用 API 将导航栏状态改为显示（navStatus: 0 -> 1）
        resp = category_service.update_nav_status([category_id], 1)
        assert resp.ok, f"修改导航栏状态API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"修改导航栏状态失败: {resp.json}"

        # 5. 数据库验证 - nav_status 已更新为 1
        sql_verify = """
            SELECT nav_status FROM pms_product_category WHERE id = %s
        """
        db_result = db.query(sql_verify, (category_id,))
        assert db_result[0]["nav_status"] == 1, \
            f"nav_status 更新失败: 期望 1, 实际 {db_result[0]['nav_status']}"

        # 6. 调用 API 删除分类
        resp = category_service.delete_category(category_id)
        assert resp.ok, f"删除分类API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"删除分类失败: {resp.json}"

        # 7. 数据库验证 - 分类已被删除
        sql_delete = """
            SELECT COUNT(*) AS cnt FROM pms_product_category WHERE id = %s
        """
        db_result = db.query(sql_delete, (category_id,))
        assert db_result[0]["cnt"] == 0, f"分类未被删除: ID={category_id}"
