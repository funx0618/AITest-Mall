"""
App Coupon Service - 前台商城优惠券相关接口封装
职责：通过 HTTP 请求操作优惠券数据
对应 Controller：UmsMemberCouponController
Base path：/member/coupon
"""

from playwright.sync_api import APIRequestContext
from api.clients.api_client import ApiClient
from api.clients.api_response import ApiResponse
from config.settings import APP_API_BASE_URL


class AppCouponService(ApiClient):
    """前台商城优惠券 API 封装，对应 UmsMemberCouponController"""

    def __init__(self, api_context: APIRequestContext, token: str):
        super().__init__(api_context, token, base_url=APP_API_BASE_URL)

    # ==================== UmsMemberCouponController ====================

    def add_coupon(self, coupon_id: int) -> ApiResponse:
        """领取优惠券
        POST /member/coupon/add/{couponId}
        """
        return self.post(f"/member/coupon/add/{coupon_id}")

    def list_coupon_history(self, use_status: int | None = None) -> ApiResponse:
        """优惠券领取记录
        GET /member/coupon/listHistory
        """
        params = {"useStatus": use_status} if use_status is not None else None
        return self.get("/member/coupon/listHistory", params=params)

    def list_coupon(self, use_status: int = 0) -> ApiResponse:
        """按状态获取会员优惠券
        GET /member/coupon/list
        use_status: 0=未使用, 1=已使用, 2=已过期
        """
        return self.get("/member/coupon/list", params={"useStatus": use_status})

    def list_cart_coupon(self, coupon_type: int = 1) -> ApiResponse:
        """购物车相关优惠券
        GET /member/coupon/list/cart/{type}
        type: 0=不可用, 1=可用
        """
        return self.get(f"/member/coupon/list/cart/{coupon_type}")

    def list_coupon_by_product(self, product_id: int) -> ApiResponse:
        """指定商品可用优惠券
        GET /member/coupon/listByProduct/{productId}
        """
        return self.get(f"/member/coupon/listByProduct/{product_id}")
