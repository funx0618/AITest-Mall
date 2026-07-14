"""
Admin Product Category Service - 后台管理商品分类相关接口封装
职责：通过 HTTP 请求操作商品分类数据
对应 Controller：PmsProductCategoryController
Base path：/productCategory
"""

from playwright.sync_api import APIRequestContext
from api.clients.api_client import ApiClient
from api.clients.api_response import ApiResponse
from config.settings import ADMIN_API_BASE_URL


class AdminProductCategoryService(ApiClient):
    """后台管理商品分类 API 封装，对应 PmsProductCategoryController"""

    def __init__(self, api_context: APIRequestContext, token: str):
        super().__init__(api_context, token, base_url=ADMIN_API_BASE_URL)

    # ==================== PmsProductCategoryController ====================

    def get_category_list(self, parent_id: int, page_num: int = 1, page_size: int = 5) -> ApiResponse:
        """分页查询商品分类
        GET /productCategory/list/{parentId}
        """
        params = {"pageNum": page_num, "pageSize": page_size}
        return self.get(f"/productCategory/list/{parent_id}", params=params)

    def get_category_detail(self, category_id: int) -> ApiResponse:
        """根据 ID 获取商品分类
        GET /productCategory/{id}
        """
        return self.get(f"/productCategory/{category_id}")

    def get_list_with_children(self) -> ApiResponse:
        """查询所有一级分类及子分类
        GET /productCategory/list/withChildren
        """
        return self.get("/productCategory/list/withChildren")

    def create_category(self, category_param: dict) -> ApiResponse:
        """添加商品分类
        POST /productCategory/create
        请求体：PmsProductCategoryParam
        """
        return self.post("/productCategory/create", json_data=category_param)

    def update_category(self, category_id: int, category_param: dict) -> ApiResponse:
        """修改商品分类
        POST /productCategory/update/{id}
        请求体：PmsProductCategoryParam
        """
        return self.post(f"/productCategory/update/{category_id}", json_data=category_param)

    def delete_category(self, category_id: int) -> ApiResponse:
        """删除商品分类
        POST /productCategory/delete/{id}
        """
        return self.post(f"/productCategory/delete/{category_id}")

    def update_nav_status(self, ids: list[int], nav_status: int) -> ApiResponse:
        """修改导航栏显示状态
        POST /productCategory/update/navStatus
        nav_status: 0=不显示, 1=显示
        """
        ids_str = ",".join(str(i) for i in ids)
        return self.post(f"/productCategory/update/navStatus?ids={ids_str}&navStatus={nav_status}")

    def update_show_status(self, ids: list[int], show_status: int) -> ApiResponse:
        """修改显示状态
        POST /productCategory/update/showStatus
        show_status: 0=不显示, 1=显示
        """
        ids_str = ",".join(str(i) for i in ids)
        return self.post(f"/productCategory/update/showStatus?ids={ids_str}&showStatus={show_status}")
