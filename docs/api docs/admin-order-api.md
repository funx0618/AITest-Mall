# Mall Admin Service — 订单相关 API Reference

> **Base URL:** `http://localhost:8080`
> **Swagger UI:** `http://localhost:8080/swagger-ui.html`
> **认证方式:** JWT Token（Header: `Authorization: Bearer <token>`）

---

## 目录

| # | Controller | 说明 | 接口数 |
|---|-----------|------|:------:|
| 1 | [OmsOrderController](#1-omsordercontroller--订单管理) | 订单管理 | 8 |
| 2 | [OmsOrderReturnApplyController](#2-omsorderreturnapplycontroller--退货申请管理) | 退货申请管理 | 4 |
| 3 | [OmsOrderReturnReasonController](#3-omsorderreturnreasoncontroller--退货原因管理) | 退货原因管理 | 6 |
| 4 | [OmsOrderSettingController](#4-omsordersettingcontroller--订单设置管理) | 订单设置管理 | 2 |

**合计：4 个 Controller，20 个接口**

---

## 1. `OmsOrderController` — 订单管理

**Base path:** `/order`

### 1.1 分页查询订单列表

```
GET /order/list
```

**涉及表：** `oms_order`

**Request Params:**

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `orderSn` | `String` | `@RequestParam` | — | 订单编号 |
| `receiverKeyword` | `String` | `@RequestParam` | — | 收货人姓名/号码 |
| `status` | `Integer` | `@RequestParam` | — | 订单状态：`0`→待付款；`1`→待发货；`2`→已发货；`3`→已完成；`4`→已关闭；`5`→无效订单 |
| `orderType` | `Integer` | `@RequestParam` | — | 订单类型：`0`→正常订单；`1`→秒杀订单 |
| `sourceType` | `Integer` | `@RequestParam` | — | 订单来源：`0`→PC订单；`1`→app订单 |
| `createTime` | `String` | `@RequestParam` | — | 订单提交时间 |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页条数 |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |

### 1.2 获取订单详情

```
GET /order/{id}
```

**涉及表：** `oms_order`, `oms_order_item`, `oms_order_operate_history`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 订单ID |

**返回：** `OmsOrderDetail`（继承 `OmsOrder`，含订单商品列表和操作记录列表）

### 1.3 批量发货

```
POST /order/update/delivery
```

**涉及表：** `oms_order`, `oms_order_operate_history`

**Request Body:** `application/json` — `List<OmsOrderDeliveryParam>`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `orderId` | `Long` | `@RequestBody` | 订单ID |
| `deliveryCompany` | `String` | `@RequestBody` | 物流公司 |
| `deliverySn` | `String` | `@RequestBody` | 物流单号 |

### 1.4 批量关闭订单

```
POST /order/update/close
```

**涉及表：** `oms_order`, `oms_order_operate_history`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 订单ID列表 |
| `note` | `String` | `@RequestParam` | 操作备注 |

### 1.5 批量删除订单

```
POST /order/delete
```

**涉及表：** `oms_order`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 订单ID列表 |

### 1.6 修改收货人信息

```
POST /order/update/receiverInfo
```

**涉及表：** `oms_order`, `oms_order_operate_history`

**Request Body:** `application/json` — `OmsReceiverInfoParam`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `orderId` | `Long` | `@RequestBody` | 订单ID |
| `receiverName` | `String` | `@RequestBody` | 收货人姓名 |
| `receiverPhone` | `String` | `@RequestBody` | 收货人电话 |
| `receiverPostCode` | `String` | `@RequestBody` | 收货人邮编 |
| `receiverDetailAddress` | `String` | `@RequestBody` | 详细地址 |
| `receiverProvince` | `String` | `@RequestBody` | 省份/直辖市 |
| `receiverCity` | `String` | `@RequestBody` | 城市 |
| `receiverRegion` | `String` | `@RequestBody` | 区 |
| `status` | `Integer` | `@RequestBody` | 订单状态：`0`→待付款；`1`→待发货；`2`→已发货；`3`→已完成；`4`→已关闭；`5`→无效订单 |

### 1.7 修改订单费用信息

```
POST /order/update/moneyInfo
```

**涉及表：** `oms_order`, `oms_order_operate_history`

**Request Body:** `application/json` — `OmsMoneyInfoParam`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `orderId` | `Long` | `@RequestBody` | 订单ID |
| `freightAmount` | `BigDecimal` | `@RequestBody` | 运费金额 |
| `discountAmount` | `BigDecimal` | `@RequestBody` | 管理员后台调整订单所使用的折扣金额 |
| `status` | `Integer` | `@RequestBody` | 订单状态：`0`→待付款；`1`→待发货；`2`→已发货；`3`→已完成；`4`→已关闭；`5`→无效订单 |

### 1.8 修改订单备注

```
POST /order/update/note
```

**涉及表：** `oms_order`, `oms_order_operate_history`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@RequestParam` | 订单ID |
| `note` | `String` | `@RequestParam` | 订单备注 |
| `status` | `Integer` | `@RequestParam` | 订单状态：`0`→待付款；`1`→待发货；`2`→已发货；`3`→已完成；`4`→已关闭；`5`→无效订单 |

---

## 2. `OmsOrderReturnApplyController` — 退货申请管理

**Base path:** `/returnApply`

### 2.1 分页查询退货申请

```
GET /returnApply/list
```

**涉及表：** `oms_order_return_apply`

**Request Params:**

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `id` | `Long` | `@RequestParam` | — | 服务单号 |
| `receiverKeyword` | `String` | `@RequestParam` | — | 收货人姓名/号码 |
| `status` | `Integer` | `@RequestParam` | — | 申请状态：`0`→待处理；`1`→退货中；`2`→已完成；`3`→已拒绝 |
| `createTime` | `String` | `@RequestParam` | — | 申请时间 |
| `handleMan` | `String` | `@RequestParam` | — | 处理人员 |
| `handleTime` | `String` | `@RequestParam` | — | 处理时间 |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页条数 |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |

### 2.2 获取退货申请详情

```
GET /returnApply/{id}
```

**涉及表：** `oms_order_return_apply`, `oms_company_address`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 退货申请ID |

**返回：** `OmsOrderReturnApplyResult`（继承 `OmsOrderReturnApply`，含公司收货地址信息）

### 2.3 批量删除退货申请

```
POST /returnApply/delete
```

**涉及表：** `oms_order_return_apply`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 退货申请ID列表 |

### 2.4 修改退货申请状态

```
POST /returnApply/update/status/{id}
```

**涉及表：** `oms_order_return_apply`

**路径参数：**

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 退货申请ID |

**Request Body:** `application/json` — `OmsUpdateStatusParam`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@RequestBody` | 服务单号 |
| `companyAddressId` | `Long` | `@RequestBody` | 收货地址关联ID |
| `returnAmount` | `BigDecimal` | `@RequestBody` | 确认退款金额 |
| `handleNote` | `String` | `@RequestBody` | 处理备注 |
| `handleMan` | `String` | `@RequestBody` | 处理人 |
| `receiveNote` | `String` | `@RequestBody` | 收货备注 |
| `receiveMan` | `String` | `@RequestBody` | 收货人 |
| `status` | `Integer` | `@RequestBody` | 申请状态：`1`→退货中；`2`→已完成；`3`→已拒绝 |

---

## 3. `OmsOrderReturnReasonController` — 退货原因管理

**Base path:** `/returnReason`

### 3.1 分页查询退货原因

```
GET /returnReason/list
```

**涉及表：** `oms_order_return_reason`

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页条数 |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |

### 3.2 获取退货原因详情

```
GET /returnReason/{id}
```

**涉及表：** `oms_order_return_reason`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 退货原因ID |

### 3.3 添加退货原因

```
POST /returnReason/create
```

**涉及表：** `oms_order_return_reason`

**Request Body:** `application/json` — `OmsOrderReturnReason`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `name` | `String` | `@RequestBody` | 退货类型名称 |
| `sort` | `Integer` | `@RequestBody` | 排序 |
| `status` | `Integer` | `@RequestBody` | 状态：`0`→不启用；`1`→启用 |

### 3.4 修改退货原因

```
POST /returnReason/update/{id}
```

**涉及表：** `oms_order_return_reason`

**路径参数：**

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 退货原因ID |

**Request Body:** `application/json` — `OmsOrderReturnReason`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `name` | `String` | `@RequestBody` | 退货类型名称 |
| `sort` | `Integer` | `@RequestBody` | 排序 |
| `status` | `Integer` | `@RequestBody` | 状态：`0`→不启用；`1`→启用 |

### 3.5 批量删除退货原因

```
POST /returnReason/delete
```

**涉及表：** `oms_order_return_reason`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `ids` | `List<Long>` | `@RequestParam` | 退货原因ID列表 |

### 3.6 批量启用/停用退货原因

```
POST /returnReason/update/status
```

**涉及表：** `oms_order_return_reason`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `status` | `Integer` | `@RequestParam` | 状态：`0`→不启用；`1`→启用 |
| `ids` | `List<Long>` | `@RequestParam` | 退货原因ID列表 |

---

## 4. `OmsOrderSettingController` — 订单设置管理

**Base path:** `/orderSetting`

### 4.1 获取订单设置详情

```
GET /orderSetting/{id}
```

**涉及表：** `oms_order_setting`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 订单设置ID |

### 4.2 修改订单设置

```
POST /orderSetting/update/{id}
```

**涉及表：** `oms_order_setting`

**路径参数：**

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 订单设置ID |

**Request Body:** `application/json` — `OmsOrderSetting`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `flashOrderOvertime` | `Integer` | `@RequestBody` | 秒杀订单超时关闭时间（分） |
| `normalOrderOvertime` | `Integer` | `@RequestBody` | 正常订单超时时间（分） |
| `confirmOvertime` | `Integer` | `@RequestBody` | 发货后自动确认收货时间（天） |
| `finishOvertime` | `Integer` | `@RequestBody` | 自动完成交易时间，不能申请售后（天） |
| `commentOvertime` | `Integer` | `@RequestBody` | 订单完成后自动好评时间（天） |

---

## 数据模型速查

### `OmsOrder` — 订单主表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 订单ID |
| `memberId` | `Long` | 会员ID |
| `couponId` | `Long` | 优惠券ID |
| `orderSn` | `String` | 订单编号 |
| `createTime` | `Date` | 提交时间 |
| `memberUsername` | `String` | 用户帐号 |
| `totalAmount` | `BigDecimal` | 订单总金额 |
| `payAmount` | `BigDecimal` | 应付金额（实际支付金额） |
| `freightAmount` | `BigDecimal` | 运费金额 |
| `promotionAmount` | `BigDecimal` | 促销优化金额（促销价、满减、阶梯价） |
| `integrationAmount` | `BigDecimal` | 积分抵扣金额 |
| `couponAmount` | `BigDecimal` | 优惠券抵扣金额 |
| `discountAmount` | `BigDecimal` | 管理员后台调整订单使用的折扣金额 |
| `payType` | `Integer` | 支付方式：`0`→未支付；`1`→支付宝；`2`→微信 |
| `sourceType` | `Integer` | 订单来源：`0`→PC订单；`1`→app订单 |
| `status` | `Integer` | 订单状态：`0`→待付款；`1`→待发货；`2`→已发货；`3`→已完成；`4`→已关闭；`5`→无效订单 |
| `orderType` | `Integer` | 订单类型：`0`→正常订单；`1`→秒杀订单 |
| `deliveryCompany` | `String` | 物流公司（配送方式） |
| `deliverySn` | `String` | 物流单号 |
| `autoConfirmDay` | `Integer` | 自动确认时间（天） |
| `integration` | `Integer` | 可以获得的积分 |
| `growth` | `Integer` | 可以活动的成长值 |
| `promotionInfo` | `String` | 活动信息 |
| `billType` | `Integer` | 发票类型：`0`→不开发票；`1`→电子发票；`2`→纸质发票 |
| `billHeader` | `String` | 发票抬头 |
| `billContent` | `String` | 发票内容 |
| `billReceiverPhone` | `String` | 收票人电话 |
| `billReceiverEmail` | `String` | 收票人邮箱 |
| `receiverName` | `String` | 收货人姓名 |
| `receiverPhone` | `String` | 收货人电话 |
| `receiverPostCode` | `String` | 收货人邮编 |
| `receiverProvince` | `String` | 省份/直辖市 |
| `receiverCity` | `String` | 城市 |
| `receiverRegion` | `String` | 区 |
| `receiverDetailAddress` | `String` | 详细地址 |
| `note` | `String` | 订单备注 |
| `confirmStatus` | `Integer` | 确认收货状态：`0`→未确认；`1`→已确认 |
| `deleteStatus` | `Integer` | 删除状态：`0`→未删除；`1`→已删除 |
| `useIntegration` | `Integer` | 下单时使用的积分 |
| `paymentTime` | `Date` | 支付时间 |
| `deliveryTime` | `Date` | 发货时间 |
| `receiveTime` | `Date` | 确认收货时间 |
| `commentTime` | `Date` | 评价时间 |
| `modifyTime` | `Date` | 修改时间 |

### `OmsOrderItem` — 订单商品明细表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 订单商品ID |
| `orderId` | `Long` | 订单ID |
| `orderSn` | `String` | 订单编号 |
| `productId` | `Long` | 商品ID |
| `productPic` | `String` | 商品图片 |
| `productName` | `String` | 商品名称 |
| `productBrand` | `String` | 商品品牌 |
| `productSn` | `String` | 商品编码 |
| `productPrice` | `BigDecimal` | 销售价格 |
| `productQuantity` | `Integer` | 购买数量 |
| `productSkuId` | `Long` | 商品SKU编号 |
| `productSkuCode` | `String` | 商品SKU条码 |
| `productCategoryId` | `Long` | 商品分类ID |
| `promotionName` | `String` | 商品促销名称 |
| `promotionAmount` | `BigDecimal` | 商品促销分解金额 |
| `couponAmount` | `BigDecimal` | 优惠券优惠分解金额 |
| `integrationAmount` | `BigDecimal` | 积分优惠分解金额 |
| `realAmount` | `BigDecimal` | 该商品经过优惠后的分解金额 |
| `giftIntegration` | `Integer` | 赠送积分 |
| `giftGrowth` | `Integer` | 赠送成长值 |
| `productAttr` | `String` | 商品销售属性：[{'key':'颜色','value':'红色'},{'key':'容量','value':'4G'}] |

### `OmsOrderOperateHistory` — 订单操作历史表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 记录ID |
| `orderId` | `Long` | 订单ID |
| `operateMan` | `String` | 操作人：用户；系统；后台管理员 |
| `createTime` | `Date` | 操作时间 |
| `orderStatus` | `Integer` | 订单状态：`0`→待付款；`1`→待发货；`2`→已发货；`3`→已完成；`4`→已关闭；`5`→无效订单 |
| `note` | `String` | 备注 |

### `OmsOrderReturnApply` — 退货申请表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 退货申请ID |
| `orderId` | `Long` | 订单ID |
| `companyAddressId` | `Long` | 收货地址表ID |
| `productId` | `Long` | 退货商品ID |
| `orderSn` | `String` | 订单编号 |
| `createTime` | `Date` | 申请时间 |
| `memberUsername` | `String` | 会员用户名 |
| `returnAmount` | `BigDecimal` | 退款金额 |
| `returnName` | `String` | 退货人姓名 |
| `returnPhone` | `String` | 退货人电话 |
| `status` | `Integer` | 申请状态：`0`→待处理；`1`→退货中；`2`→已完成；`3`→已拒绝 |
| `handleTime` | `Date` | 处理时间 |
| `productPic` | `String` | 商品图片 |
| `productName` | `String` | 商品名称 |
| `productBrand` | `String` | 商品品牌 |
| `productAttr` | `String` | 商品销售属性：颜色：红色；尺码：xl |
| `productCount` | `Integer` | 退货数量 |
| `productPrice` | `BigDecimal` | 商品单价 |
| `productRealPrice` | `BigDecimal` | 商品实际支付单价 |
| `reason` | `String` | 原因 |
| `description` | `String` | 描述 |
| `proofPics` | `String` | 凭证图片，以逗号隔开 |
| `handleNote` | `String` | 处理备注 |
| `handleMan` | `String` | 处理人员 |
| `receiveMan` | `String` | 收货人 |
| `receiveTime` | `Date` | 收货时间 |
| `receiveNote` | `String` | 收货备注 |

### `OmsOrderReturnReason` — 退货原因表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 退货原因ID |
| `name` | `String` | 退货类型名称 |
| `sort` | `Integer` | 排序 |
| `status` | `Integer` | 状态：`0`→不启用；`1`→启用 |
| `createTime` | `Date` | 添加时间 |

### `OmsOrderSetting` — 订单设置表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 订单设置ID |
| `flashOrderOvertime` | `Integer` | 秒杀订单超时关闭时间（分） |
| `normalOrderOvertime` | `Integer` | 正常订单超时时间（分） |
| `confirmOvertime` | `Integer` | 发货后自动确认收货时间（天） |
| `finishOvertime` | `Integer` | 自动完成交易时间，不能申请售后（天） |
| `commentOvertime` | `Integer` | 订单完成后自动好评时间（天） |

### `OmsCompanyAddress` — 公司收货地址表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 地址ID |
| `addressName` | `String` | 地址名称 |
| `sendStatus` | `Integer` | 默认发货地址：`0`→否；`1`→是 |
| `receiveStatus` | `Integer` | 是否默认收货地址：`0`→否；`1`→是 |
| `name` | `String` | 收发货人姓名 |
| `phone` | `String` | 收货人电话 |
| `province` | `String` | 省/直辖市 |
| `city` | `String` | 市 |
| `region` | `String` | 区 |
| `detailAddress` | `String` | 详细地址 |

---

## 涉及表/存储汇总

### MySQL 表（7 张）

| 表名 | 说明 | 使用 Controller |
|------|------|-----------------|
| `oms_order` | 订单主表 | OmsOrderController |
| `oms_order_item` | 订单商品明细表 | OmsOrderController |
| `oms_order_operate_history` | 订单操作历史表 | OmsOrderController |
| `oms_order_return_apply` | 退货申请表 | OmsOrderReturnApplyController |
| `oms_order_return_reason` | 退货原因表 | OmsOrderReturnReasonController |
| `oms_order_setting` | 订单设置表（超时时间等） | OmsOrderSettingController |
| `oms_company_address` | 公司收货地址表（退货用） | OmsOrderReturnApplyController |

---

## 汇总

| 类别 | Controller 数 | 接口数 |
|------|:---:|:---:|
| 订单管理 | 1 | 8 |
| 退货申请管理 | 1 | 4 |
| 退货原因管理 | 1 | 6 |
| 订单设置管理 | 1 | 2 |
| **合计** | **4** | **20** |
