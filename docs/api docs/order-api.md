# Mall Order API Reference

## Admin Service (`mall-admin`) — 4 Controllers, 17 Endpoints

### 1. `OmsOrderController` — 订单管理
**Base path:** `/order`

| Method | Path | 说明 |
|--------|------|------|
| `GET` | `/order/list` | 分页查询订单列表 |
| `GET` | `/order/{id}` | 获取订单详情（订单信息、商品、日志） |
| `POST` | `/order/update/delivery` | 批量发货 |
| `POST` | `/order/update/close` | 批量关闭订单 |
| `POST` | `/order/delete` | 批量删除订单 |
| `POST` | `/order/update/receiverInfo` | 修改收货人信息 |
| `POST` | `/order/update/moneyInfo` | 修改订单费用信息 |
| `POST` | `/order/update/note` | 修改订单备注 |

### 2. `OmsOrderReturnApplyController` — 退货申请管理
**Base path:** `/returnApply`

| Method | Path | 说明 |
|--------|------|------|
| `GET` | `/returnApply/list` | 分页查询退货申请 |
| `GET` | `/returnApply/{id}` | 获取退货申请详情 |
| `POST` | `/returnApply/delete` | 批量删除退货申请 |
| `POST` | `/returnApply/update/status/{id}` | 修改退货申请状态 |

### 3. `OmsOrderReturnReasonController` — 退货原因管理
**Base path:** `/returnReason`

| Method | Path | 说明 |
|--------|------|------|
| `GET` | `/returnReason/list` | 分页查询退货原因 |
| `GET` | `/returnReason/{id}` | 获取退货原因详情 |
| `POST` | `/returnReason/create` | 添加退货原因 |
| `POST` | `/returnReason/update/{id}` | 修改退货原因 |
| `POST` | `/returnReason/delete` | 批量删除退货原因 |
| `POST` | `/returnReason/update/status` | 批量启用/停用退货原因 |

### 4. `OmsOrderSettingController` — 订单设置管理
**Base path:** `/orderSetting`

| Method | Path | 说明 |
|--------|------|------|
| `GET` | `/orderSetting/{id}` | 获取订单设置详情 |
| `POST` | `/orderSetting/update/{id}` | 修改订单设置 |

---

## Portal/App Service (`mall-portal`) — 2 Controllers, 11 Endpoints

### 1. `OmsPortalOrderController` — 用户订单管理
**Base path:** `/order`

| Method | Path | 说明 |
|--------|------|------|
| `POST` | `/order/generateConfirmOrder` | 根据购物车生成确认单信息 |
| `POST` | `/order/generateOrder` | 提交订单（从购物车下单） |
| `POST` | `/order/paySuccess` | 支付成功回调 |
| `POST` | `/order/cancelTimeOutOrder` | 自动取消超时订单 |
| `POST` | `/order/cancelOrder` | 发送延迟消息取消单个订单 |
| `GET` | `/order/list` | 按状态分页查询用户订单（-1全部/0未付款/1未发货/2已发货/3已完成/4已关闭） |
| `GET` | `/order/detail/{orderId}` | 获取订单详情 |
| `POST` | `/order/cancelUserOrder` | 用户取消订单 |
| `POST` | `/order/confirmReceiveOrder` | 用户确认收货 |
| `POST` | `/order/deleteOrder` | 用户删除订单 |

### 2. `OmsPortalOrderReturnApplyController` — 用户退货申请
**Base path:** `/returnApply`

| Method | Path | 说明 |
|--------|------|------|
| `POST` | `/returnApply/create` | 用户提交退货申请 |

---

## 汇总

| 服务 | Controller 数 | 接口数 |
|------|:---:|:---:|
| **Admin** (`mall-admin`) | 4 | 17 |
| **Portal** (`mall-portal`) | 2 | 11 |
| **合计** | **6** | **28** |
