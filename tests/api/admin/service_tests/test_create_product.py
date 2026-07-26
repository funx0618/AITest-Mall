"""
创建商品 API 测试用例
职责：验证后台管理创建商品接口
对应 API 文档：docs/api docs/admin-product-api.md
涉及表：pms_product, pms_member_price, pms_product_ladder, pms_product_full_reduction,
        pms_sku_stock, pms_product_attribute_value, cms_subject_product_relation,
        cms_prefrence_area_product_relation
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
    data = load_yaml("api/test_create_product.yaml")
    return data[request.function.__name__]


class TestCreateProduct:
    """创建商品接口测试"""

    def test_create_product(self, product_service: AdminProductService, db: DBClient, test_data: dict):
        """创建商品后验证 pms_product 表数据落库正确"""
        # 0. 查询数据库中已有的品牌和分类（确保外键有效）
        brand_row = db.query("SELECT id FROM pms_brand LIMIT 1")
        assert len(brand_row) > 0, "数据库中无品牌数据，无法创建商品"
        brand_id = brand_row[0]["id"]

        category_row = db.query("SELECT id FROM pms_product_category WHERE product_unit IS NOT NULL LIMIT 1")
        assert len(category_row) > 0, "数据库中无商品分类数据，无法创建商品"
        product_category_id = category_row[0]["id"]

        # 1. 构造请求参数
        product_param = {
            "brandId": brand_id,
            "productCategoryId": product_category_id,
            "name": test_data["name"],
            "productSn": test_data["product_sn"],
            "price": test_data["price"],
            "originalPrice": test_data["original_price"],
            "stock": test_data["stock"],
            "lowStock": test_data["low_stock"],
            "subTitle": test_data["sub_title"],
            "pic": test_data["pic"],
            "albumPics": test_data["album_pics"],
            "unit": test_data["unit"],
            "weight": test_data["weight"],
            "sort": test_data["sort"],
            "publishStatus": test_data["publish_status"],
            "newStatus": test_data["new_status"],
            "recommandStatus": test_data["recommand_status"],
            "verifyStatus": test_data["verify_status"],
            "deleteStatus": 0,
            "promotionType": test_data["promotion_type"],
            "giftGrowth": test_data["gift_growth"],
            "giftPoint": test_data["gift_point"],
            "serviceIds": test_data["service_ids"],
            "keywords": test_data["keywords"],
            "note": test_data["note"],
            "detailTitle": test_data["detail_title"],
            "detailDesc": test_data["detail_desc"],
            "detailHtml": test_data["detail_html"],
            "detailMobileHtml": test_data["detail_mobile_html"],
            "memberPriceList": test_data["member_price_list"],
            "productLadderList": test_data["product_ladder_list"],
            "productFullReductionList": test_data["product_full_reduction_list"],
            "skuStockList": test_data["sku_stock_list"],
            "productAttributeValueList": test_data["product_attribute_value_list"],
            "subjectProductRelationList": test_data["subject_product_relation_list"],
            "prefrenceAreaProductRelationList": test_data["prefrence_area_product_relation_list"],
        }

        # 2. API 创建商品
        resp = product_service.create_product(product_param)
        assert resp.ok, f"API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"创建商品失败: {resp.json}"

        # 3. 数据库验证 - pms_product 表
        sql = """
            SELECT * FROM pms_product
            WHERE product_sn = %s
            ORDER BY id DESC
            LIMIT 1
        """
        db_result = db.query(sql, (test_data["product_sn"],))
        assert len(db_result) > 0, f"数据库中未找到商品: product_sn={test_data['product_sn']}"
        product = db_result[0]
        product_id = product["id"]

        assert product["name"] == test_data["name"], \
            f"商品名称不匹配: 期望 {test_data['name']}, 实际 {product['name']}"
        assert float(product["price"]) == test_data["price"], \
            f"商品价格不匹配: 期望 {test_data['price']}, 实际 {product['price']}"
        assert float(product["original_price"]) == test_data["original_price"], \
            f"市场价不匹配: 期望 {test_data['original_price']}, 实际 {product['original_price']}"
        assert product["stock"] == test_data["stock"], \
            f"库存不匹配: 期望 {test_data['stock']}, 实际 {product['stock']}"
        assert product["low_stock"] == test_data["low_stock"], \
            f"库存预警值不匹配: 期望 {test_data['low_stock']}, 实际 {product['low_stock']}"
        assert product["sub_title"] == test_data["sub_title"], \
            f"副标题不匹配: 期望 {test_data['sub_title']}, 实际 {product['sub_title']}"
        assert product["unit"] == test_data["unit"], \
            f"单位不匹配: 期望 {test_data['unit']}, 实际 {product['unit']}"
        assert product["sort"] == test_data["sort"], \
            f"排序不匹配: 期望 {test_data['sort']}, 实际 {product['sort']}"
        assert product["publish_status"] == test_data["publish_status"], \
            f"上架状态不匹配: 期望 {test_data['publish_status']}, 实际 {product['publish_status']}"
        assert product["new_status"] == test_data["new_status"], \
            f"新品状态不匹配: 期望 {test_data['new_status']}, 实际 {product['new_status']}"
        assert product["recommand_status"] == test_data["recommand_status"], \
            f"推荐状态不匹配: 期望 {test_data['recommand_status']}, 实际 {product['recommand_status']}"
        assert product["verify_status"] == test_data["verify_status"], \
            f"审核状态不匹配: 期望 {test_data['verify_status']}, 实际 {product['verify_status']}"
        assert product["brand_id"] == brand_id, \
            f"品牌ID不匹配: 期望 {brand_id}, 实际 {product['brand_id']}"
        assert product["product_category_id"] == product_category_id, \
            f"分类ID不匹配: 期望 {product_category_id}, 实际 {product['product_category_id']}"
        assert product["keywords"] == test_data["keywords"], \
            f"关键字不匹配: 期望 {test_data['keywords']}, 实际 {product['keywords']}"
        assert product["note"] == test_data["note"], \
            f"备注不匹配: 期望 {test_data['note']}, 实际 {product['note']}"
        assert product["delete_status"] == 0, \
            f"删除状态异常: 期望 0, 实际 {product['delete_status']}"

        # 4. 清理：软删除测试商品
        resp = product_service.update_delete_status([product_id], 1)
        assert resp.ok, f"清理商品API请求失败: HTTP {resp.status_code}"
        assert resp.code == 200, f"清理商品失败: {resp.json}"

        # 5. 数据库验证商品已软删除
        sql_del = """
            SELECT delete_status FROM pms_product WHERE id = %s
        """
        db_result = db.query(sql_del, (product_id,))
        assert db_result[0]["delete_status"] == 1, f"商品未被软删除: ID={product_id}"
