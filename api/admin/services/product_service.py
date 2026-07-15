"""
Admin Product Service - 后台管理商品相关接口封装
职责：通过 HTTP 请求操作商品数据
对应 Controller：PmsProductController
Base path：/product
"""

from playwright.sync_api import APIRequestContext
from api.clients.api_client import ApiClient
from api.clients.api_response import ApiResponse
from config.settings import ADMIN_API_BASE_URL


class AdminProductService(ApiClient):
    """后台管理商品 API 封装，对应 PmsProductController"""

    def __init__(self, api_context: APIRequestContext, token: str):
        super().__init__(api_context, token, base_url=ADMIN_API_BASE_URL)

    # ==================== PmsProductController ====================

    def create_product(self, product_param: dict) -> ApiResponse:
        """创建商品
        POST /product/create
        请求体：PmsProductParam
        """
        return self.post("/product/create", json_data=product_param)

    def get_update_info(self, product_id: int) -> ApiResponse:
        """获取商品编辑信息
        GET /product/updateInfo/{id}
        """
        return self.get(f"/product/updateInfo/{product_id}")

    def update_product(self, product_id: int, product_param: dict) -> ApiResponse:
        """更新商品
        POST /product/update/{id}
        请求体：PmsProductParam
        """
        return self.post(f"/product/update/{product_id}", json_data=product_param)

    def get_product_list(
        self,
        keyword: str | None = None,
        product_sn: str | None = None,
        product_category_id: int | None = None,
        brand_id: int | None = None,
        publish_status: int | None = None,
        verify_status: int | None = None,
        page_num: int = 1,
        page_size: int = 5,
    ) -> ApiResponse:
        """分页查询商品
        GET /product/list
        """
        params: dict = {"pageNum": page_num, "pageSize": page_size}
        if keyword is not None:
            params["keyword"] = keyword
        if product_sn is not None:
            params["productSn"] = product_sn
        if product_category_id is not None:
            params["productCategoryId"] = product_category_id
        if brand_id is not None:
            params["brandId"] = brand_id
        if publish_status is not None:
            params["publishStatus"] = publish_status
        if verify_status is not None:
            params["verifyStatus"] = verify_status
        return self.get("/product/list", params=params)

    def get_simple_list(self, keyword: str) -> ApiResponse:
        """按名称/货号模糊查询
        GET /product/simpleList
        """
        params = {"keyword": keyword}
        return self.get("/product/simpleList", params=params)

    def update_verify_status(self, ids: list[int], verify_status: int, detail: str = "") -> ApiResponse:
        """批量修改审核状态
        POST /product/update/verifyStatus
        verify_status: 0=未审核, 1=审核通过
        """
        ids_str = ",".join(str(i) for i in ids)
        return self.post(
            f"/product/update/verifyStatus?ids={ids_str}&verifyStatus={verify_status}&detail={detail}"
        )

    def update_publish_status(self, ids: list[int], publish_status: int) -> ApiResponse:
        """批量上下架商品
        POST /product/update/publishStatus
        publish_status: 0=下架, 1=上架
        """
        ids_str = ",".join(str(i) for i in ids)
        return self.post(f"/product/update/publishStatus?ids={ids_str}&publishStatus={publish_status}")

    def update_recommend_status(self, ids: list[int], recommend_status: int) -> ApiResponse:
        """批量推荐商品
        POST /product/update/recommendStatus
        recommend_status: 0=不推荐, 1=推荐
        """
        ids_str = ",".join(str(i) for i in ids)
        return self.post(
            f"/product/update/recommendStatus?ids={ids_str}&recommendStatus={recommend_status}"
        )

    def update_new_status(self, ids: list[int], new_status: int) -> ApiResponse:
        """批量设为新品
        POST /product/update/newStatus
        new_status: 0=非新品, 1=新品
        """
        ids_str = ",".join(str(i) for i in ids)
        return self.post(f"/product/update/newStatus?ids={ids_str}&newStatus={new_status}")

    def update_delete_status(self, ids: list[int], delete_status: int) -> ApiResponse:
        """批量软删除商品
        POST /product/update/deleteStatus
        delete_status: 0=未删除, 1=已删除
        """
        ids_str = ",".join(str(i) for i in ids)
        return self.post(f"/product/update/deleteStatus?ids={ids_str}&deleteStatus={delete_status}")
