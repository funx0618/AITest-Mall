"""
App Cart Service - 前台商城购物车相关接口封装
职责：通过 HTTP 请求操作购物车数据
对应 Controller：OmsCartItemController
Base path：/cart
"""

from playwright.sync_api import APIRequestContext
from api.clients.api_client import ApiClient
from api.clients.api_response import ApiResponse
from config.settings import APP_API_BASE_URL


class AppCartService(ApiClient):
    """前台商城购物车 API 封装，对应 OmsCartItemController"""

    def __init__(self, api_context: APIRequestContext, token: str):
        super().__init__(api_context, token, base_url=APP_API_BASE_URL)

    # ==================== OmsCartItemController ====================

    def add_cart(self, product_id: int, product_sku_id: int, quantity: int) -> ApiResponse:
        """添加商品到购物车
        POST /cart/add
        请求体：OmsCartItem
        """
        json_data = {
            "productId": product_id,
            "productSkuId": product_sku_id,
            "quantity": quantity,
        }
        return self.post("/cart/add", json_data=json_data)

    def list_cart(self) -> ApiResponse:
        """获取购物车列表
        GET /cart/list
        """
        return self.get("/cart/list")

    def list_cart_promotion(self, cart_ids: list[int] | None = None) -> ApiResponse:
        """获取购物车列表（含促销信息）
        GET /cart/list/promotion
        """
        params = None
        if cart_ids:
            params = {"cartIds": cart_ids}
        return self.get("/cart/list/promotion", params=params)

    def update_quantity(self, cart_id: int, quantity: int) -> ApiResponse:
        """修改购物车商品数量
        GET /cart/update/quantity
        """
        params = {"id": cart_id, "quantity": quantity}
        return self.get("/cart/update/quantity", params=params)

    def get_product(self, product_id: int) -> ApiResponse:
        """获取商品 SKU/属性信息
        GET /cart/getProduct/{productId}
        """
        return self.get(f"/cart/getProduct/{product_id}")

    def update_attr(self, cart_item: dict) -> ApiResponse:
        """修改购物车商品规格
        POST /cart/update/attr
        请求体：OmsCartItem
        """
        return self.post("/cart/update/attr", json_data=cart_item)

    def delete_cart(self, ids: list[int]) -> ApiResponse:
        """删除购物车商品
        POST /cart/delete
        ids 为 @RequestParam，通过 URL 查询参数传递
        """
        query = "&".join(f"ids={id_}" for id_ in ids)
        return self.post(f"/cart/delete?{query}")

    def clear_cart(self) -> ApiResponse:
        """清空购物车
        POST /cart/clear
        """
        return self.post("/cart/clear")
