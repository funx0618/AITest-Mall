# Mall Order API Reference

## Admin Service (`mall-admin`) — 4 Controllers, 17 Endpoints

### 1. `OmsOrderController` — 订单管理
**Base path:** `/order`

| Method | Path | 说明 | 涉及表 |
|--------|------|------|--------|
| `GET` | `/order/list` | 分页查询订单列表 | `oms_order` |
| `GET` | `/order/{id}` | 获取订单详情 | `oms_order`, `oms_order_item`, `oms_order_operate_history` |
| `POST` | `/order/update/delivery` | 批量发货 | `oms_order`, `oms_order_operate_history` |
| `POST` | `/order/update/close` | 批量关闭订单 | `oms_order`, `oms_order_operate_history` |
| `POST` | `/order/delete` | 批量删除订单 | `oms_order` |
| `POST` | `/order/update/receiverInfo` | 修改收货人信息 | `oms_order`, `oms_order_operate_history` |
| `POST` | `/order/update/moneyInfo` | 修改订单费用信息 | `oms_order`, `oms_order_operate_history` |
| `POST` | `/order/update/note` | 修改订单备注 | `oms_order`, `oms_order_operate_history` |

### 2. `OmsOrderReturnApplyController` — 退货申请管理
**Base path:** `/returnApply`

| Method | Path | 说明 | 涉及表 |
|--------|------|------|--------|
| `GET` | `/returnApply/list` | 分页查询退货申请 | `oms_order_return_apply` |
| `GET` | `/returnApply/{id}` | 获取退货申请详情 | `oms_order_return_apply`, `oms_company_address` |
| `POST` | `/returnApply/delete` | 批量删除退货申请 | `oms_order_return_apply` |
| `POST` | `/returnApply/update/status/{id}` | 修改退货申请状态 | `oms_order_return_apply` |

### 3. `OmsOrderReturnReasonController` — 退货原因管理
**Base path:** `/returnReason`

| Method | Path | 说明 | 涉及表 |
|--------|------|------|--------|
| `GET` | `/returnReason/list` | 分页查询退货原因 | `oms_order_return_reason` |
| `GET` | `/returnReason/{id}` | 获取退货原因详情 | `oms_order_return_reason` |
| `POST` | `/returnReason/create` | 添加退货原因 | `oms_order_return_reason` |
| `POST` | `/returnReason/update/{id}` | 修改退货原因 | `oms_order_return_reason` |
| `POST` | `/returnReason/delete` | 批量删除退货原因 | `oms_order_return_reason` |
| `POST` | `/returnReason/update/status` | 批量启用/停用退货原因 | `oms_order_return_reason` |

### 4. `OmsOrderSettingController` — 订单设置管理
**Base path:** `/orderSetting`

| Method | Path | 说明 | 涉及表 |
|--------|------|------|--------|
| `GET` | `/orderSetting/{id}` | 获取订单设置详情 | `oms_order_setting` |
| `POST` | `/orderSetting/update/{id}` | 修改订单设置 | `oms_order_setting` |

---

## Portal/App Service (`mall-portal`) — 2 Controllers, 11 Endpoints

### 1. `OmsPortalOrderController` — 用户订单管理
**Base path:** `/order`

| Method | Path | 说明 | 涉及表 |
|--------|------|------|--------|
| `POST` | `/order/generateConfirmOrder` | 生成确认单信息 | `ums_member`, `oms_cart_item`, `ums_member_receive_address`, `sms_coupon_history`, `sms_coupon`, `sms_coupon_product_relation`, `sms_coupon_product_category_relation`, `ums_integration_consume_setting` |
| `POST` | `/order/generateOrder` | 提交订单 | `ums_member`, `oms_cart_item`, `ums_member_receive_address`, `oms_order_setting`, `oms_order`, `oms_order_item`, `sms_coupon_history` |
| `POST` | `/order/paySuccess` | 支付成功回调 | `oms_order`, `oms_order_item`, `pms_sku_stock` |
| `POST` | `/order/cancelTimeOutOrder` | 自动取消超时订单 | `oms_order_setting`, `oms_order`, `oms_order_item`, `pms_sku_stock`, `sms_coupon_history`, `ums_member` |
| `POST` | `/order/cancelOrder` | 发送延迟消息取消订单 | `oms_order_setting` |
| `GET` | `/order/list` | 查询用户订单列表 | `ums_member`, `oms_order`, `oms_order_item` |
| `GET` | `/order/detail/{orderId}` | 获取订单详情 | `oms_order`, `oms_order_item` |
| `POST` | `/order/cancelUserOrder` | 用户取消订单 | `oms_order`, `oms_order_item`, `pms_sku_stock`, `sms_coupon_history`, `ums_member` |
| `POST` | `/order/confirmReceiveOrder` | 用户确认收货 | `ums_member`, `oms_order` |
| `POST` | `/order/deleteOrder` | 用户删除订单 | `ums_member`, `oms_order` |

### 2. `OmsPortalOrderReturnApplyController` — 用户退货申请
**Base path:** `/returnApply`

| Method | Path | 说明 | 涉及表 |
|--------|------|------|--------|
| `POST` | `/returnApply/create` | 用户提交退货申请 | `oms_order_return_apply` |

---

## 涉及表汇总

| 表名 | 说明 |
|------|------|
| `oms_order` | 订单主表 |
| `oms_order_item` | 订单商品明细表 |
| `oms_order_operate_history` | 订单操作历史表 |
| `oms_order_return_apply` | 退货申请表 |
| `oms_order_return_reason` | 退货原因表 |
| `oms_order_setting` | 订单设置表（超时时间等） |
| `oms_company_address` | 公司收货地址表（退货用） |
| `oms_cart_item` | 购物车表 |
| `pms_sku_stock` | 商品 SKU 库存表 |
| `sms_coupon` | 优惠券表 |
| `sms_coupon_history` | 优惠券使用记录表 |
| `sms_coupon_product_relation` | 优惠券-商品关联表 |
| `sms_coupon_product_category_relation` | 优惠券-分类关联表 |
| `ums_member` | 会员表 |
| `ums_member_receive_address` | 会员收货地址表 |
| `ums_integration_consume_setting` | 积分消费设置表 |

---

## 汇总

| 服务 | Controller 数 | 接口数 |
|------|:---:|:---:|
| **Admin** (`mall-admin`) | 4 | 17 |
| **Portal** (`mall-portal`) | 2 | 11 |
| **合计** | **6** | **28** |
