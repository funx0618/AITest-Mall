"""
Admin Coupon Service - 后台管理优惠券相关接口封装
职责：通过 HTTP 请求操作优惠券数据
对应 Controller：SmsCouponController、SmsCouponHistoryController
Base path：/coupon、/couponHistory
"""

from playwright.sync_api import APIRequestContext
from api.clients.api_client import ApiClient
from api.clients.api_response import ApiResponse
from config.settings import ADMIN_API_BASE_URL


class AdminCouponService(ApiClient):
    """后台管理优惠券 API 封装，对应 SmsCouponController / SmsCouponHistoryController"""

    def __init__(self, api_context: APIRequestContext, token: str):
        super().__init__(api_context, token, base_url=ADMIN_API_BASE_URL)

    # ==================== SmsCouponController ====================

    def create_coupon(self, coupon_param: dict) -> ApiResponse:
        """创建优惠券
        POST /coupon/create
        请求体：SmsCouponParam
        """
        return self.post("/coupon/create", json_data=coupon_param)

    def delete_coupon(self, coupon_id: int) -> ApiResponse:
        """删除优惠券
        POST /coupon/delete/{id}
        """
        return self.post(f"/coupon/delete/{coupon_id}")

    def update_coupon(self, coupon_id: int, coupon_param: dict) -> ApiResponse:
        """修改优惠券
        POST /coupon/update/{id}
        请求体：SmsCouponParam
        """
        return self.post(f"/coupon/update/{coupon_id}", json_data=coupon_param)

    def list_coupon(
        self,
        name: str = None,
        coupon_type: int = None,
        page_num: int = 1,
        page_size: int = 5,
    ) -> ApiResponse:
        """分页查询优惠券列表
        GET /coupon/list
        """
        params = {"pageNum": page_num, "pageSize": page_size}
        if name is not None:
            params["name"] = name
        if coupon_type is not None:
            params["type"] = coupon_type
        return self.get("/coupon/list", params=params)

    def get_coupon_detail(self, coupon_id: int) -> ApiResponse:
        """获取优惠券详情
        GET /coupon/{id}
        """
        return self.get(f"/coupon/{coupon_id}")

    # ==================== SmsCouponHistoryController ====================

    def list_coupon_history(
        self,
        coupon_id: int = None,
        use_status: int = None,
        order_sn: str = None,
        page_num: int = 1,
        page_size: int = 5,
    ) -> ApiResponse:
        """分页查询优惠券领取记录
        GET /couponHistory/list
        """
        params = {"pageNum": page_num, "pageSize": page_size}
        if coupon_id is not None:
            params["couponId"] = coupon_id
        if use_status is not None:
            params["useStatus"] = use_status
        if order_sn is not None:
            params["orderSn"] = order_sn
        return self.get("/couponHistory/list", params=params)
