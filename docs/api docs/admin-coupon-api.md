# Mall Admin Service — 优惠券相关 API Reference

> **Base URL:** `http://localhost:8080`
> **Swagger UI:** `http://localhost:8080/swagger-ui.html`
> **认证方式:** JWT Token（Header: `Authorization: Bearer <token>`）

---

## 目录

| # | Controller | 说明 | 接口数 |
|---|-----------|------|:------:|
| 1 | [SmsCouponController](#1-smscouponcontroller--优惠券管理) | 优惠券管理 | 5 |
| 2 | [SmsCouponHistoryController](#2-smscouponhistorycontroller--优惠券领取记录) | 优惠券领取记录 | 1 |

**合计：2 个 Controller，6 个接口**

---

## 1. `SmsCouponController` — 优惠券管理

**Base path:** `/coupon`

### 1.1 添加优惠券

```
POST /coupon/create
```

**涉及表：** `sms_coupon`, `sms_coupon_product_relation`, `sms_coupon_product_category_relation`

**Request Body:** `application/json` — `SmsCouponParam`（继承 `SmsCoupon`，含关联列表）

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `name` | `String` | `@RequestBody` | 优惠券名称 |
| `type` | `Integer` | `@RequestBody` | 优惠券类型：`0`→全场赠券；`1`→会员赠券；`2`→购物赠券；`3`→注册赠券 |
| `platform` | `Integer` | `@RequestBody` | 使用平台：`0`→全部；`1`→移动；`2`→PC |
| `amount` | `BigDecimal` | `@RequestBody` | 金额 |
| `perLimit` | `Integer` | `@RequestBody` | 每人限领张数 |
| `minPoint` | `BigDecimal` | `@RequestBody` | 使用门槛（`0` 表示无门槛） |
| `startTime` | `Date` | `@RequestBody` | 开始时间 |
| `endTime` | `Date` | `@RequestBody` | 结束时间 |
| `useType` | `Integer` | `@RequestBody` | 使用类型：`0`→全场通用；`1`→指定分类；`2`→指定商品 |
| `note` | `String` | `@RequestBody` | 备注 |
| `publishCount` | `Integer` | `@RequestBody` | 发行数量 |
| `enableTime` | `Date` | `@RequestBody` | 可领取日期 |
| `code` | `String` | `@RequestBody` | 优惠码 |
| `memberLevel` | `Integer` | `@RequestBody` | 可领取会员类型：`0`→无限制 |
| `productRelationList` | `List<SmsCouponProductRelation>` | `@RequestBody` | 关联商品列表（`useType=2` 时使用） |
| `productCategoryRelationList` | `List<SmsCouponProductCategoryRelation>` | `@RequestBody` | 关联分类列表（`useType=1` 时使用） |

### 1.2 删除优惠券

```
POST /coupon/delete/{id}
```

**涉及表：** `sms_coupon`, `sms_coupon_product_relation`, `sms_coupon_product_category_relation`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 优惠券 ID |

> 级联删除关联的商品/分类关系记录。

### 1.3 修改优惠券

```
POST /coupon/update/{id}
```

**涉及表：** `sms_coupon`, `sms_coupon_product_relation`, `sms_coupon_product_category_relation`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 优惠券 ID |
| `couponParam` | `SmsCouponParam` | `@RequestBody` | 优惠券参数（同 1.1） |

> 先删除旧关联，再插入新关联。

### 1.4 分页查询优惠券列表

```
GET /coupon/list
```

**涉及表：** `sms_coupon`

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `name` | `String` | `@RequestParam` | — | 优惠券名称（模糊匹配） |
| `type` | `Integer` | `@RequestParam` | — | 优惠券类型（同 1.1） |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页条数 |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |

### 1.5 获取优惠券详情

```
GET /coupon/{id}
```

**涉及表：** `sms_coupon`, `sms_coupon_product_relation`, `sms_coupon_product_category_relation`

| 参数 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `id` | `Long` | `@PathVariable` | 优惠券 ID |

返回 `SmsCouponParam`，包含优惠券基本信息及关联的商品/分类列表。

---

## 2. `SmsCouponHistoryController` — 优惠券领取记录

**Base path:** `/couponHistory`

### 2.1 分页查询领取记录

```
GET /couponHistory/list
```

**涉及表：** `sms_coupon_history`

| 参数 | 类型 | 位置 | 默认值 | 说明 |
|------|------|------|--------|------|
| `couponId` | `Long` | `@RequestParam` | — | 优惠券 ID |
| `useStatus` | `Integer` | `@RequestParam` | — | 使用状态：`0`→未使用；`1`→已使用；`2`→已过期 |
| `orderSn` | `String` | `@RequestParam` | — | 订单编号 |
| `pageSize` | `Integer` | `@RequestParam` | `5` | 每页条数 |
| `pageNum` | `Integer` | `@RequestParam` | `1` | 页码 |

---

## 数据模型速查

### `SmsCoupon` — 优惠券

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 优惠券 ID |
| `type` | `Integer` | 类型：`0`→全场赠券；`1`→会员赠券；`2`→购物赠券；`3`→注册赠券 |
| `name` | `String` | 优惠券名称 |
| `platform` | `Integer` | 使用平台：`0`→全部；`1`→移动；`2`→PC |
| `count` | `Integer` | 数量 |
| `amount` | `BigDecimal` | 金额 |
| `perLimit` | `Integer` | 每人限领张数 |
| `minPoint` | `BigDecimal` | 使用门槛（`0` 表示无门槛） |
| `startTime` | `Date` | 开始时间 |
| `endTime` | `Date` | 结束时间 |
| `useType` | `Integer` | 使用类型：`0`→全场通用；`1`→指定分类；`2`→指定商品 |
| `note` | `String` | 备注 |
| `publishCount` | `Integer` | 发行数量 |
| `useCount` | `Integer` | 已使用数量 |
| `receiveCount` | `Integer` | 领取数量 |
| `enableTime` | `Date` | 可领取日期 |
| `code` | `String` | 优惠码 |
| `memberLevel` | `Integer` | 可领取会员类型：`0`→无限制 |

### `SmsCouponParam` — 优惠券创建/编辑参数（继承 `SmsCoupon`）

| 字段 | 类型 | 说明 |
|------|------|------|
| `productRelationList` | `List<SmsCouponProductRelation>` | 关联商品列表 |
| `productCategoryRelationList` | `List<SmsCouponProductCategoryRelation>` | 关联商品分类列表 |

### `SmsCouponProductRelation` — 优惠券-商品关联

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 关联 ID |
| `couponId` | `Long` | 优惠券 ID |
| `productId` | `Long` | 商品 ID |
| `productName` | `String` | 商品名称 |
| `productSn` | `String` | 商品编码 |

### `SmsCouponProductCategoryRelation` — 优惠券-分类关联

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 关联 ID |
| `couponId` | `Long` | 优惠券 ID |
| `productCategoryId` | `Long` | 商品分类 ID |
| `productCategoryName` | `String` | 分类名称 |
| `parentCategoryName` | `String` | 父分类名称 |

### `SmsCouponHistory` — 优惠券领取记录

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `Long` | 记录 ID |
| `couponId` | `Long` | 优惠券 ID |
| `memberId` | `Long` | 会员 ID |
| `couponCode` | `String` | 优惠码 |
| `memberNickname` | `String` | 领取人昵称 |
| `getType` | `Integer` | 获取类型：`0`→后台赠送；`1`→主动获取 |
| `createTime` | `Date` | 领取时间 |
| `useStatus` | `Integer` | 使用状态：`0`→未使用；`1`→已使用；`2`→已过期 |
| `useTime` | `Date` | 使用时间 |
| `orderId` | `Long` | 订单 ID |
| `orderSn` | `String` | 订单编号 |

---

## 涉及表/存储汇总

### MySQL 表（4 张）

| 表名 | 说明 |
|------|------|
| `sms_coupon` | 优惠券表 |
| `sms_coupon_history` | 优惠券领取记录表 |
| `sms_coupon_product_relation` | 优惠券-商品关联表 |
| `sms_coupon_product_category_relation` | 优惠券-分类关联表 |

---

## 汇总

| 类别 | Controller 数 | 接口数 |
|------|:---:|:---:|
| 优惠券管理 | 1 | 5 |
| 领取记录 | 1 | 1 |
| **合计** | **2** | **6** |
