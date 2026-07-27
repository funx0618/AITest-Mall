# Mall App (Portal) Service — 完整 API Reference

> **Base URL:** `http://localhost:8085`
> **Swagger UI:** `http://localhost:8085/swagger-ui.html`
> **认证方式:** JWT Token（Header: `Authorization: Bearer <token>`）

---

## 目录

| # | Controller | 说明 | 接口数 |
|---|-----------|------|:------:|
| 1 | [UmsMemberController](#1-umsmembercontroller--会员登录注册) | 会员登录/注册 | 6 |
| 2 | [HomeController](#2-homecontroller--首页内容) | 首页内容 | 6 |
| 3 | [PmsPortalProductController](#3-pmsportalproductcontroller--商品) | 商品搜索/详情 | 3 |
| 4 | [PmsPortalBrandController](#4-pmsportalbrandcontroller--品牌) | 品牌 | 3 |
| 5 | [OmsCartItemController](#5-omscartitemcontroller--购物车) | 购物车 | 8 |
| 6 | [UmsMemberReceiveAddressController](#6-umsmemberreceiveaddresscontroller--收货地址) | 收货地址 | 5 |
| 7 | [UmsMemberCouponController](#7-umsmembercouponcontroller--优惠券) | 优惠券 | 5 |
| 8 | [OmsPortalOrderController](#8-omsportalordercontroller--订单) | 订单 | 10 |
| 9 | [OmsPortalOrderReturnApplyController](#9-omsportalorderreturnapplycontroller--退货申请) | 退货申请 | 1 |
| 10 | [AlipayController](#10-alipaycontroller--支付宝支付) | 支付宝支付 | 4 |
| 11 | [MemberAttentionController](#11-memberattentioncontroller--品牌关注) | 品牌关注 | 5 |
| 12 | [MemberProductCollectionController](#12-memberproductcollectioncontroller--商品收藏) | 商品收藏 | 5 |
| 13 | [MemberReadHistoryController](#13-memberreadhistorycontroller--浏览历史) | 浏览历史 | 4 |

**合计：13 个 Controller，65 个接口**

---

## 1. `UmsMemberController` — 会员登录/注册

**Base path:** `/sso`

### 1.1 会员注册

```
POST /sso/register
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `username` | `String` | `@RequestParam` | — | 用户名 |
| `password` | `String` | `@RequestParam` | — | 密码 |
| `telephone` | `String` | `@RequestParam` | — | 手机号 |
| `authCode` | `String` | `@RequestParam` | — | 验证码 |

### 1.2 会员登录

```
POST /sso/login
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `username` | `String` | `@RequestParam` | — | 用户名 |
| `password` | `String` | `@RequestParam` | — | 密码 |

### 1.3 获取当前登录会员信息

```
GET /sso/info
```

需要认证。返回 `UmsMember` 对象。

### 1.4 获取验证码

```
GET /sso/getAuthCode
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `telephone` | `String` | `@RequestParam` | — | 手机号 |

### 1.5 修改密码

```
POST /sso/updatePassword
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `telephone` | `String` | `@RequestParam` | — | 手机号 |
| `password` | `String` | `@RequestParam` | — | 新密码 |
| `authCode` | `String` | `@RequestParam` | — | 验证码 |

### 1.6 刷新 Token

```
GET /sso/refreshToken
```

需要认证。从 Header 中读取当前 Token 并刷新。

---

## 2. `HomeController` — 首页内容

**Base path:** `/home`

### 2.1 首页内容信息展示

```
GET /home/content
```

一次性返回首页所有模块数据。

### 2.2 分页推荐商品

```
GET /home/recommendProductList
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |
| `pageSize` | `Integer` | `@RequestParam` | `4` | 每页条数 |

### 2.3 获取首页商品分类

```
GET /home/productCateList/{parentId}
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `parentId` | `Long` | `@PathVariable` | — | 父分类 ID |

### 2.4 根据分类获取专题

```
GET /home/subjectList
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `cateId` | `Long` | `@RequestParam` | — | 分类 ID |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |
| `pageSize` | `Integer` | `@RequestParam` | `4` | 每页条数 |

### 2.5 分页获取人气推荐商品

```
GET /home/hotProductList
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |
| `pageSize` | `Integer` | `@RequestParam` | `6` | 每页条数 |

### 2.6 分页获取新品推荐商品

```
GET /home/newProductList
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |
| `pageSize` | `Integer` | `@RequestParam` | `6` | 每页条数 |

---

## 3. `PmsPortalProductController` — 商品

**Base path:** `/product`

### 3.1 综合搜索、筛选、排序

```
GET /product/search
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `keyword` | `String` | `@RequestParam` | — | 搜索关键词 |
| `brandId` | `Long` | `@RequestParam` | — | 品牌 ID |
| `productCategoryId` | `Long` | `@RequestParam` | — | 商品分类 ID |
| `pageNum` | `Integer` | `@RequestParam` | `0` | 页码 |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页条数 |
| `sort` | `Integer` | `@RequestParam` | `0` | 排序：`0`→综合；`1`→新品；`2`→销量；`3`→价格↑；`4`→价格↓ |

### 3.2 商品分类树

```
GET /product/categoryTreeList
```

### 3.3 商品详情

```
GET /product/detail/{id}
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `id` | `Long` | `@PathVariable` | — | 商品 ID |

---

## 4. `PmsPortalBrandController` — 品牌

**Base path:** `/brand`

### 4.1 分页推荐品牌

```
GET /brand/recommendList
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |
| `pageSize` | `Integer` | `@RequestParam` | `6` | 每页条数 |

### 4.2 品牌详情

```
GET /brand/detail/{brandId}
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `brandId` | `Long` | `@PathVariable` | — | 品牌 ID |

### 4.3 品牌下分页商品

```
GET /brand/productList
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `brandId` | `Long` | `@RequestParam` | — | 品牌 ID |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |
| `pageSize` | `Integer` | `@RequestParam` | `6` | 每页条数 |

---

## 5. `OmsCartItemController` — 购物车

**Base path:** `/cart`

### 5.1 添加商品到购物车

```
POST /cart/add
```

**Request Body:** `application/json` — `OmsCartItem`

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `productId` | `Long` | `@RequestBody` | — | 商品 ID |
| `productSkuId` | `Long` | `@RequestBody` | — | SKU ID |
| `quantity` | `Integer` | `@RequestBody` | — | 数量 |

### 5.2 获取购物车列表

```
GET /cart/list
```

### 5.3 获取购物车列表（含促销信息）

```
GET /cart/list/promotion
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `cartIds` | `List<Long>` | `@RequestParam` | — | 指定购物车 ID，不传返回全部 |

### 5.4 修改购物车商品数量

```
GET /cart/update/quantity
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `id` | `Long` | `@RequestParam` | — | 购物车项 ID |
| `quantity` | `Integer` | `@RequestParam` | — | 新数量 |

### 5.5 获取商品 SKU/属性信息

```
GET /cart/getProduct/{productId}
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `productId` | `Long` | `@PathVariable` | — | 商品 ID |

### 5.6 修改购物车商品规格

```
POST /cart/update/attr
```

**Request Body:** `application/json` — `OmsCartItem`（含新规格）

### 5.7 删除购物车商品

```
POST /cart/delete
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `ids` | `List<Long>` | `@RequestParam` | — | 购物车项 ID 列表 |

### 5.8 清空购物车

```
POST /cart/clear
```

---

## 6. `UmsMemberReceiveAddressController` — 收货地址

**Base path:** `/member/address`

### 6.1 添加收货地址

```
POST /member/address/add
```

**Request Body:** `application/json` — `UmsMemberReceiveAddress`

### 6.2 删除收货地址

```
POST /member/address/delete/{id}
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `id` | `Long` | `@PathVariable` | — | 地址 ID |

### 6.3 修改收货地址

```
POST /member/address/update/{id}
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `id` | `Long` | `@PathVariable` | — | 地址 ID |

**Request Body:** `application/json` — `UmsMemberReceiveAddress`（同 6.1）

### 6.4 获取所有收货地址

```
GET /member/address/list
```

### 6.5 获取收货地址详情

```
GET /member/address/{id}
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `id` | `Long` | `@PathVariable` | — | 地址 ID |

---

## 7. `UmsMemberCouponController` — 优惠券

**Base path:** `/member/coupon`

### 7.1 领取优惠券

```
POST /member/coupon/add/{couponId}
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `couponId` | `Long` | `@PathVariable` | — | 优惠券 ID |

### 7.2 优惠券领取记录

```
GET /member/coupon/listHistory
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `useStatus` | `Integer` | `@RequestParam` | — | `0`→未使用；`1`→已使用；`2`→已过期 |

### 7.3 按状态获取会员优惠券

```
GET /member/coupon/list
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `useStatus` | `Integer` | `@RequestParam` | — | `0`→未使用；`1`→已使用；`2`→已过期 |

### 7.4 购物车相关优惠券

```
GET /member/coupon/list/cart/{type}
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `type` | `Integer` | `@PathVariable` | — | `0`→不可用；`1`→可用 |

### 7.5 指定商品可用优惠券

```
GET /member/coupon/listByProduct/{productId}
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `productId` | `Long` | `@PathVariable` | — | 商品 ID |

---

## 8. `OmsPortalOrderController` — 订单

**Base path:** `/order`

### 8.1 生成确认单

```
POST /order/generateConfirmOrder
```

**Request Body:** `application/json` — 购物车 ID 数组 `[1, 2, 3]`

### 8.2 提交订单

```
POST /order/generateOrder
```

**Request Body:** `application/json` — `OrderParam`

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `memberReceiveAddressId` | `Long` | `@RequestBody` | — | 收货地址 ID |
| `couponId` | `Long` | `@RequestBody` | — | 优惠券 ID |
| `useIntegration` | `Integer` | `@RequestBody` | — | 使用积分数 |
| `payType` | `Integer` | `@RequestBody` | — | 支付方式：`1`→支付宝；`2`→微信 |
| `cartIds` | `List<Long>` | `@RequestBody` | — | 购物车 ID 列表 |

### 8.3 支付成功回调

```
POST /order/paySuccess
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `orderId` | `Long` | `@RequestParam` | — | 订单 ID |
| `payType` | `Integer` | `@RequestParam` | — | 支付方式 |

### 8.4 自动取消超时订单

```
POST /order/cancelTimeOutOrder
```

系统定时调用，无参数。

### 8.5 发送延迟消息取消订单

```
POST /order/cancelOrder
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `orderId` | `Long` | `Model Attribute` | — | 订单 ID |

### 8.6 查询用户订单列表

```
GET /order/list
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `status` | `Integer` | `@RequestParam` | `-1` | `-1`→全部；`0`→待付款；`1`→待发货；`2`→已发货；`3`→已完成；`4`→已关闭 |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页条数 |

### 8.7 获取订单详情

```
GET /order/detail/{orderId}
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `orderId` | `Long` | `@PathVariable` | — | 订单 ID |

### 8.8 用户取消订单

```
POST /order/cancelUserOrder
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `orderId` | `Long` | `Model Attribute` | — | 订单 ID |

### 8.9 用户确认收货

```
POST /order/confirmReceiveOrder
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `orderId` | `Long` | `Model Attribute` | — | 订单 ID |

### 8.10 用户删除订单

```
POST /order/deleteOrder
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `orderId` | `Long` | `Model Attribute` | — | 订单 ID |

---

## 9. `OmsPortalOrderReturnApplyController` — 退货申请

**Base path:** `/returnApply`

### 9.1 提交退货申请

```
POST /returnApply/create
```

**Request Body:** `application/json` — `OmsOrderReturnApplyParam`

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `orderId` | `Long` | `@RequestBody` | — | 订单 ID |
| `productId` | `Long` | `@RequestBody` | — | 退货商品 ID |
| `orderSn` | `String` | `@RequestBody` | — | 订单编号 |
| `memberUsername` | `String` | `@RequestBody` | — | 会员用户名 |
| `returnName` | `String` | `@RequestBody` | — | 退货人姓名 |
| `returnPhone` | `String` | `@RequestBody` | — | 退货人电话 |
| `productPic` | `String` | `@RequestBody` | — | 商品图片 URL |
| `productName` | `String` | `@RequestBody` | — | 商品名称 |
| `productBrand` | `String` | `@RequestBody` | — | 商品品牌 |
| `productAttr` | `String` | `@RequestBody` | — | 销售属性，格式：`颜色：红色；尺码：xl` |
| `productCount` | `Integer` | `@RequestBody` | — | 退货数量 |
| `productPrice` | `BigDecimal` | `@RequestBody` | — | 商品单价 |
| `productRealPrice` | `BigDecimal` | `@RequestBody` | — | 实际支付单价 |
| `reason` | `String` | `@RequestBody` | — | 退货原因 |
| `description` | `String` | `@RequestBody` | — | 详细描述 |
| `proofPics` | `String` | `@RequestBody` | — | 凭证图片（逗号分隔） |

---

## 10. `AlipayController` — 支付宝支付

**Base path:** `/alipay`

### 10.1 PC 网页支付

```
GET /alipay/pay
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `outTradeNo` | `String` | `Model Attribute` | — | 商户订单号（保持唯一） |
| `subject` | `String` | `Model Attribute` | — | 订单标题 |
| `totalAmount` | `BigDecimal` | `Model Attribute` | — | 订单金额（元） |

**Response:** `text/html` — 支付宝支付表单 HTML

### 10.2 手机网页支付

```
GET /alipay/webPay
```

参数同 10.1。**Response:** `text/html` — 支付宝 WAP 支付页面

### 10.3 支付宝异步回调

```
POST /alipay/notify
```

支付宝服务端主动通知。Content-Type: `application/x-www-form-urlencoded`。

| 关键参数 | 说明 |
|----------|------|
| `out_trade_no` | 商户订单号 |
| `trade_no` | 支付宝交易号 |
| `trade_status` | 交易状态（`TRADE_SUCCESS` = 支付成功） |
| `total_amount` | 订单金额 |
| `sign` | 签名 |

**Response:** 字符串 `success` 或 `failure`

### 10.4 查询交易状态

```
GET /alipay/query
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `outTradeNo` | `String` | `Model Attribute` | — | 商户订单号（与 tradeNo 二选一） |
| `tradeNo` | `String` | `Model Attribute` | — | 支付宝交易号 |

---

## 11. `MemberAttentionController` — 品牌关注

**Base path:** `/member/attention` · **存储：MongoDB**

### 11.1 添加品牌关注

```
POST /member/attention/add
```

**Request Body:** `application/json` — `MemberBrandAttention`

### 11.2 取消品牌关注

```
POST /member/attention/delete
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `brandId` | `Long` | `Model Attribute` | — | 品牌 ID |

### 11.3 分页查询品牌关注列表

```
GET /member/attention/list
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页条数 |

### 11.4 获取品牌关注详情

```
GET /member/attention/detail
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `brandId` | `Long` | `@RequestParam` | — | 品牌 ID |

### 11.5 清空品牌关注

```
POST /member/attention/clear
```

---

## 12. `MemberProductCollectionController` — 商品收藏

**Base path:** `/member/productCollection` · **存储：MongoDB**

### 12.1 添加商品收藏

```
POST /member/productCollection/add
```

**Request Body:** `application/json` — `MemberProductCollection`

### 12.2 删除商品收藏

```
POST /member/productCollection/delete
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `productId` | `Long` | `Model Attribute` | — | 商品 ID |

### 12.3 分页获取收藏列表

```
GET /member/productCollection/list
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页条数 |

### 12.4 获取收藏详情

```
GET /member/productCollection/detail
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `productId` | `Long` | `@RequestParam` | — | 商品 ID |

### 12.5 清空收藏

```
POST /member/productCollection/clear
```

---

## 13. `MemberReadHistoryController` — 浏览历史

**Base path:** `/member/readHistory` · **存储：MongoDB**

### 13.1 创建浏览记录

```
POST /member/readHistory/create
```

**Request Body:** `application/json` — `MemberReadHistory`

### 13.2 删除浏览记录

```
POST /member/readHistory/delete
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `ids` | `List<String>` | `@RequestParam` | — | 记录 ID 列表 |

### 13.3 清空浏览历史

```
POST /member/readHistory/clear
```

### 13.4 分页获取浏览记录

```
GET /member/readHistory/list
```

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页条数 |

---

## 数据模型速查

### `OmsOrder` — 订单主表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 订单 ID |
| `memberId` | `Long` | 会员 ID |
| `couponId` | `Long` | 优惠券 ID |
| `orderSn` | `String` | 订单编号 |
| `createTime` | `Date` | 提交时间 |
| `totalAmount` | `BigDecimal` | 订单总金额 |
| `payAmount` | `BigDecimal` | 应付金额 |
| `freightAmount` | `BigDecimal` | 运费 |
| `promotionAmount` | `BigDecimal` | 促销优惠金额 |
| `integrationAmount` | `BigDecimal` | 积分抵扣金额 |
| `couponAmount` | `BigDecimal` | 优惠券抵扣金额 |
| `discountAmount` | `BigDecimal` | 管理员调整折扣 |
| `payType` | `Integer` | 支付方式：`0`→未支付；`1`→支付宝；`2`→微信 |
| `sourceType` | `Integer` | 来源：`0`→PC；`1`→APP |
| `status` | `Integer` | 状态：`0`→待付款；`1`→待发货；`2`→已发货；`3`→已完成；`4`→已关闭；`5`→无效 |
| `orderType` | `Integer` | 类型：`0`→正常；`1`→秒杀 |
| `deliveryCompany` | `String` | 物流公司 |
| `deliverySn` | `String` | 物流单号 |
| `receiverName` | `String` | 收货人姓名 |
| `receiverPhone` | `String` | 收货人电话 |
| `receiverProvince` | `String` | 省份 |
| `receiverCity` | `String` | 城市 |
| `receiverRegion` | `String` | 区 |
| `receiverDetailAddress` | `String` | 详细地址 |
| `note` | `String` | 订单备注 |
| `confirmStatus` | `Integer` | 确认状态：`0`→未确认；`1`→已确认 |
| `deleteStatus` | `Integer` | 删除状态：`0`→未删除；`1`→已删除 |
| `useIntegration` | `Integer` | 使用积分数 |
| `paymentTime` | `Date` | 支付时间 |
| `deliveryTime` | `Date` | 发货时间 |
| `receiveTime` | `Date` | 确认收货时间 |
| `commentTime` | `Date` | 评价时间 |

### `OmsOrderItem` — 订单商品明细

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 订单商品 ID |
| `orderId` | `Long` | 订单 ID |
| `productId` | `Long` | 商品 ID |
| `productPic` | `String` | 商品图片 |
| `productName` | `String` | 商品名称 |
| `productBrand` | `String` | 品牌 |
| `productPrice` | `BigDecimal` | 销售价格 |
| `productQuantity` | `Integer` | 数量 |
| `productSkuId` | `Long` | SKU ID |
| `productCategoryId` | `Long` | 分类 ID |
| `promotionName` | `String` | 促销名称 |
| `promotionAmount` | `BigDecimal` | 促销优惠金额 |
| `couponAmount` | `BigDecimal` | 优惠券优惠金额 |
| `integrationAmount` | `BigDecimal` | 积分优惠金额 |
| `realAmount` | `BigDecimal` | 优惠后实际金额 |
| `productAttr` | `String` | 销售属性 JSON |

### `OmsCartItem` — 购物车

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 购物车项 ID |
| `productId` | `Long` | 商品 ID |
| `productSkuId` | `Long` | SKU ID |
| `memberId` | `Long` | 会员 ID |
| `quantity` | `Integer` | 数量 |
| `price` | `BigDecimal` | 价格 |
| `productPic` | `String` | 商品图片 |
| `productName` | `String` | 商品名称 |
| `productSubTitle` | `String` | 副标题 |
| `deleteStatus` | `Integer` | 删除状态 |

### `UmsMemberReceiveAddress` — 收货地址

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 地址 ID |
| `memberId` | `Long` | 会员 ID |
| `name` | `String` | 收货人姓名 |
| `phoneNumber` | `String` | 电话 |
| `defaultStatus` | `Integer` | 是否默认：`0`→否；`1`→是 |
| `postCode` | `String` | 邮编 |
| `province` | `String` | 省份 |
| `city` | `String` | 城市 |
| `region` | `String` | 区 |
| `detailAddress` | `String` | 详细地址 |

### `AliPayParam` — 支付宝参数

| 字段 | 类型 | 说明 |
|------|------|------|
| `outTradeNo` | `String` | 商户订单号 |
| `subject` | `String` | 订单标题 |
| `totalAmount` | `BigDecimal` | 订单金额（元） |

---

## 涉及表/存储汇总

### MySQL 表（25 张）

| 表名 | 说明 |
|------|------|
| `oms_order` | 订单主表 |
| `oms_order_item` | 订单商品明细表 |
| `oms_order_setting` | 订单设置表 |
| `oms_order_return_apply` | 退货申请表 |
| `oms_cart_item` | 购物车表 |
| `pms_product` | 商品表 |
| `pms_product_category` | 商品分类表 |
| `pms_brand` | 品牌表 |
| `pms_product_attribute` | 商品属性表 |
| `pms_product_attribute_value` | 商品属性值表 |
| `pms_sku_stock` | SKU 库存表 |
| `pms_product_ladder` | 商品阶梯价格表 |
| `pms_product_full_reduction` | 商品满减表 |
| `ums_member` | 会员表 |
| `ums_member_level` | 会员等级表 |
| `ums_member_receive_address` | 会员收货地址表 |
| `ums_integration_consume_setting` | 积分消费设置表 |
| `sms_coupon` | 优惠券表 |
| `sms_coupon_history` | 优惠券使用记录表 |
| `sms_coupon_product_relation` | 优惠券-商品关联表 |
| `sms_coupon_product_category_relation` | 优惠券-分类关联表 |
| `sms_home_advertise` | 首页广告表 |
| `sms_flash_promotion` | 秒杀活动表 |
| `sms_flash_promotion_session` | 秒杀场次表 |
| `cms_subject` | 专题表 |

### MongoDB 集合（3 个）

| 集合名 | 说明 |
|--------|------|
| `member_brand_attention` | 品牌关注 |
| `member_product_collection` | 商品收藏 |
| `member_read_history` | 浏览历史 |

---

## 汇总

| 类别 | Controller 数 | 接口数 |
|------|:---:|:---:|
| 会员/认证 | 1 | 6 |
| 首页 | 1 | 6 |
| 商品/品牌 | 2 | 6 |
| 购物车 | 1 | 8 |
| 收货地址 | 1 | 5 |
| 优惠券 | 1 | 5 |
| 订单 | 2 | 11 |
| 支付 | 1 | 4 |
| 关注/收藏/历史 | 3 | 14 |
| **合计** | **13** | **65** |

---

## 订单状态流转

```
[提交订单] → 待付款(0) → 支付成功 → 待发货(1) → 管理员发货 → 已发货(2) → 确认收货 → 已完成(3)
                ↓                                                         ↑
            已关闭(4) ← 超时未付 / 用户取消                          自动确认到期
```

| 状态码 | 状态 | 触发方式 |
|:------:|------|----------|
| `0` | 待付款 | `POST /order/generateOrder` |
| `1` | 待发货 | `POST /order/paySuccess` |
| `2` | 已发货 | 管理员操作（`mall-admin`） |
| `3` | 已完成 | `POST /order/confirmReceiveOrder` 或自动确认 |
| `4` | 已关闭 | `POST /order/cancelUserOrder` 或超时自动取消 |
| `5` | 无效订单 | 系统标记 |
